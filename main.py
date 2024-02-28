from machine import Pin
from boatBLE import boatBLE
import boatLoRa

##################################################################
##################################################################
## Callback when data received through LoRa
def receivedLoRa(payload):
    print("Received LoRa: ", payload.message)

    # Check if BLE is connected or not
    if bluetoothLowEnergy.is_connected():
        # If BLE connected, notify
        bluetoothLowEnergy.send(payload.message)

##################################################################
##################################################################
## Callback when data received through BLE
def receivedBLE(data):
    print("Received BLE: ", data)
    # Process the received BLE message
    print(data)

##################################################################
## Callback when BLE connected to RPi 4
def connectedBLE():
    print("Connected to BoatBoat Brain!!")

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
print("BLE Initialized!!")

# Setup on board LED to let user know also if BLE connected or not 
led = Pin("LED", Pin.OUT)
led.off()

##################################################################
## main operation

# Test for LoRa
# loraModule_TX = boatLoRa.boatLoRa_TX()
# print("Boat LoRa TX Initialized!!")
# loraModule_TX.loraSenderTest()

loraModule_RX = boatLoRa.boatLoRa_RX()
print("Boat LoRa RX Initialized!!")
loraModule_RX.loraRX(receivedLoRa)

#Test for BLE
bleTtest()