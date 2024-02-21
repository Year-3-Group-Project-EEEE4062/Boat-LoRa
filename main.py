from rfReceiver import boatRF
from machine import Pin
from loraReceiver import boatLoRa

# Create instance of RF class
# Test for RF
# rf = boatRF()
# rf.nrfReceiverTest()

# Test for LoRa
loraModule = boatLoRa()
loraModule.loraReceiverTest()