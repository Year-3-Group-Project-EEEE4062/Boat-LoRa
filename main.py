from rfReceiver import boatRF
import utime
from machine import Pin

# Create instance of RF class
rf = boatRF()

# Initiate rf testing
rf.nrfReceiverTest()
