"""Test for nrf24l01 module.  Portable between MicroPython targets."""

import usys
import ustruct as struct
import utime
import uctypes
from machine import Pin, SPI, SoftSPI
from lib.rf.nrf24l01 import NRF24L01
from micropython import const

# Run nrf24l01test.responder() on responder, then nrf24l01test.initiator() on initiator

# Responder pause between receiving data and checking for further packets.
_RX_POLL_DELAY = const(15)

# Responder pauses an additional _RESPONER_SEND_DELAY ms after receiving data and before
# transmitting to allow the (remote) initiator time to get into receive mode. The
# initiator may be a slow device. Value tested with Pyboard, ESP32 and ESP8266.
_RESPONDER_SEND_DELAY = const(10)

# Set the pins for the RF module
spi = SPI(0, sck=Pin(6), mosi=Pin(7), miso=Pin(4))
cfg = {"spi": spi, "miso": 4, "mosi": 7, "sck": 6, "csn": 5, "ce": 8}

# Addresses are in little-endian format. They correspond to big-endian
# 0xf0f0f0f0e1, 0xf0f0f0f0d2
pipes = (b"\xe1\xf0\xf0\xf0\xf0", b"\xd2\xf0\xf0\xf0\xf0")


def initiator():
    csn = Pin(cfg["csn"], mode=Pin.OUT, value=1)
    ce = Pin(cfg["ce"], mode=Pin.OUT, value=0)
    spi = cfg["spi"]
    nrf = NRF24L01(spi, csn, ce, payload_size=8)

    nrf.open_tx_pipe(pipes[0])
    nrf.open_rx_pipe(1, pipes[1])
    nrf.start_listening()

    num_needed = 16
    num_successes = 0
    num_failures = 0
    led_state = 0

    print("NRF24L01 initiator mode, sending %d packets..." % num_needed)

    while num_successes < num_needed and num_failures < num_needed:
        # stop listening and send packet
        nrf.stop_listening()
        mssg = "cibai"
        print("sending:", mssg)
        try:
            nrf.send(mssg.encode('utf-8'))
        except OSError:
            pass

        # start listening again
        nrf.start_listening()

        # wait for response, with 250ms timeout
        start_time = utime.ticks_ms()
        timeout = False
        while not nrf.any() and not timeout:
            if utime.ticks_diff(utime.ticks_ms(), start_time) > 250:
                timeout = True

        if timeout:
            print("failed, response timed out")
            num_failures += 1

        else:
            # recv packet
            pingedMssg = nrf.recv().decode('utf-8')

            # print response and round-trip delay
            num_successes += 1

        # delay then loop
        utime.sleep_ms(250)

    print("initiator finished sending; successes=%d, failures=%d" % (num_successes, num_failures))

def responder():
    csn = Pin(cfg["csn"], mode=Pin.OUT, value=1)
    ce = Pin(cfg["ce"], mode=Pin.OUT, value=0)
    spi = cfg["spi"]
    nrf = NRF24L01(spi, csn, ce, payload_size=8)

    nrf.open_tx_pipe(pipes[1])
    nrf.open_rx_pipe(1, pipes[0])
    nrf.start_listening()

    print("NRF24L01 responder mode, waiting for packets... (ctrl-C to stop)")

    while True:
        # Check if any data is received
        if nrf.any():
            # While data has been received
            while nrf.any():
                buf = nrf.recv()
                mssg = buf.decode('utf-8')
                print("received:", mssg)
                utime.sleep_ms(_RX_POLL_DELAY)

            # Give initiator time to get into receive mode.
            utime.sleep_ms(_RESPONDER_SEND_DELAY)

            # Stop boat RF from listening
            nrf.stop_listening()

            # Try replying to the message to the initiator
            try:
                pingMssg = "Got it!"
                nrf.send(pingMssg.encode('utf-8'))
            except OSError:
                pass
            
            print("sent response")
            nrf.start_listening()
