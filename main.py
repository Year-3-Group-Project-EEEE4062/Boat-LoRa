from rfReceiver import boatRF
from machine import Pin
from loraReceiver import boatLoRa

# Create instance of RF class
# rf = boatRF()
loraModule = boatLoRa()

loraModule.loraReceiverTest()