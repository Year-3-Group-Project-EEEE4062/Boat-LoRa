from machine import Pin
from boatBLE import boatBLE
import boatLoRa

##################################################################
##################################################################
## Callback when data received through BLE
## RaspberryPi Pico W BLE Max byte per transmission is 20 bytes
def receivedBLE(data):
    # Process the received BLE message
    print(data)

##################################################################
## Callback when BLE connected to phone
def connectedBLE():
    print("Connected")

    # Turn ON onboard LED
    # This to indicate to user that BLE is connected
    led.on()

##################################################################
## Callback when BLE disconnected from to phone
def disconnectedBLE():
    print("Disconnected")

    # Turn OFF onboard LED
    # This to indicate to user that BLE NOT connected
    led.off()

def bleTtest():
    # Infinite loop
    while True:
        # check if BLE connected or not
        if bluetoothLowEnergy.is_connected():
            pass

##################################################################
##################################################################
## Initialization
bluetoothLowEnergy = boatBLE(connectedBLE, disconnectedBLE, receivedBLE)

# Setup on board LED to let user know also if BLE connected or not 
led = Pin("LED", Pin.OUT)
led.off()

##################################################################
## main operation

# Test for LoRa
# loraModule_TX = boatLoRa.boatLoRa_TX()
# loraModule_TX.loraSenderTest()

# loraModule_RX = boatLoRa.boatLoRa_RX()
# loraModule_RX.loraReceiverTest()

#Test for BLE
bleTtest()