from machine import Pin, UART
import sys
import ubinascii

import select

from boatLoRa import boatLoRa
##################################################################
##################################################################
## Callback wto send data to brain
def sendToBrain(mssg):
    # Convert bytearray to base64-encoded string
    base64_string = ubinascii.b2a_base64(mssg).decode('utf-8').strip()

    # Convert bytearray to byte strings
    sys.stdout.write(base64_string+'\n')

    # let the RPi4 know new data
    TX_INT.on()
    TX_INT.off()

##################################################################
##################################################################
## Initialization
# Setup on board LED to let user know also if BLE connected or not 
led = Pin("LED", Pin.OUT)
led.off()

# Set up GPIO Interrupt pin upon change in state of this pin
TX_INT = Pin(15, Pin.OUT) # White wire
TX_INT.off()

# Set up the poll object
poll_obj = select.poll()
poll_obj.register(sys.stdin, select.POLLIN)

##################################################################
## main operation
try:
    LoRa = boatLoRa(sendToBrain)
except:
    print("LoRa init error!")

led.on() # Indicate everything initialized

try:
    while True:
        # Wait for input on stdin
        poll_results = poll_obj.poll(1) # the '1' is how long it will wait for message before looping again (in microseconds)
        if poll_results:
            base64_str = sys.stdin.readline().strip()
            reply = bytearray(ubinascii.a2b_base64(base64_str))
            LoRa.sendMssg(reply)

except Exception as err:
    print(err)