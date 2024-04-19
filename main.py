from machine import Pin, UART
import sys
import select

from boatLoRa import boatLoRa
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
while True:
    try:
        LoRa = boatLoRa()
        break
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
