from machine import Pin, I2C
import time

import boatLoRa

##################################################################
##################################################################
## Callback when data received through LoRa
def receivedLoRa(payload):
    print("Received LoRa: ", payload.message)

##################################################################
##################################################################
## Callback when data received from RPi 4 (main boat brain)
def receivedI2C(pin):
    print("Received data from Brain!!")

##################################################################
##################################################################
## Initialization
# loraModule_TX = boatLoRa.boatLoRa_TX()
# print("Boat LoRa TX Initialized!!")

loraModule_RX = boatLoRa.boatLoRa_RX()
print("Boat LoRa RX Initialized!!")

# Setup on board LED to let user know also if BLE connected or not 
led = Pin("LED", Pin.OUT)
led.off()

# Setup I2C to exchange data with brain
sdaPin = Pin(14)
sclPin = Pin(15)
i2c=machine.I2C(0,sda=sdaPIN, scl=sclPIN, freq=400000)
TX_INT = Pin(12, Pin.OUT) # White wire
RX_INT = Pin(13, Pin.OUT) # Blue wire

##################################################################
## main operation

# Test for LoRa
# loraModule_TX.loraSenderTest()
loraModule_RX.loraRX(receivedLoRa)

# Set up GPIO Interrupt pin upon change in state of this pin
RX_INT.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=receivedI2C)

time.sleep(10)

while True:
    TX_INT.toggle()
    time.sleep(5)
    print("Toggled!!")
    pass