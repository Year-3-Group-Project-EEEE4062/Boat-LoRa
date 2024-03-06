from machine import Pin
import select
import sys
import time
import ubinascii

from boatLoRa import boatLoRa
##################################################################
##################################################################
## Callback when data received through LoRa
def receivedLoRa(payload):
    # Convert bytearray to base64-encoded string
    base64_string = ubinascii.b2a_base64(payload.message).decode('utf-8').strip()

    # Convert bytearray to byte strings
    sys.stdout.write(base64_string+'\n')

    # let the RPi4 know new data
    TX_INT.toggle()

##################################################################
##################################################################
## Callback when data received from RPi 4 (main boat brain)
def receivedFromBrain(pin):
    print("Received data from Brain!!")

##################################################################
##################################################################
## Initialization
# Setup on board LED to let user know also if BLE connected or not 
led = Pin("LED", Pin.OUT)
led.off()

# Set up GPIO Interrupt pin upon change in state of this pin
TX_INT = Pin(15, Pin.OUT) # White wire
RX_INT = Pin(14, Pin.IN) # Blue wire
RX_INT.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=receivedFromBrain)

print("Pico W Serial INT Initialized")

##################################################################
## main operation
LoRa = boatLoRa()
print("Boat LoRa initialized!!")

led.on() # Indicate everything initialized

try:
    while True:
        pass
except KeyboardInterrupt:
    pass