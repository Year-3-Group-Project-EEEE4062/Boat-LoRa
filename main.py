from rfReceiver import boatRF
from machine import Pin
import boatLoRa

# Create instance of RF class
# Test for RF
# rf = boatRF()
# rf.nrfReceiverTest()

# Test for LoRa
loraModule_TX = boatLoRa.boatLoRa_TX()
loraModule_TX.loraSenderTest()

loraModule_RX = boatLoRa.boatLoRa_RX()
loraModule_RX.loraReceiverTest()