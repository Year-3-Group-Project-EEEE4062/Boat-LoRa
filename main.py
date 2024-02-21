from rfReceiver import boatRF
import utime
from machine import Pin

# Create instance of RF class
rf = boatRF()

# Initiate rf testing
rf.nrfReceiverTest()

# led = Pin("LED", Pin.OUT)
# while True:
#     led.on()
#     utime.sleep_ms(100)
#     led.off()
#     utime.sleep_ms(100)
