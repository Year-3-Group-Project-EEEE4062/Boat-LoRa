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

class boatRF:
    def __init__(self):
        # Setup on board LED to let user know if message received or not
        self.led = Pin("LED", Pin.OUT)

        # Set the pins for the RF module
        self.spi = SPI(0, sck=Pin(6), mosi=Pin(7), miso=Pin(4))
        self.cfg = {"spi": self.spi, "miso": 4, "mosi": 7, "sck": 6, "csn": 5, "ce": 8}

        # Addresses are in little-endian format. They correspond to big-endian
        # 0xf0f0f0f0e1, 0xf0f0f0f0d2
        self.pipes = (b"\xe1\xf0\xf0\xf0\xf0", b"\xd2\xf0\xf0\xf0\xf0")

        self.csn = Pin(self.cfg["csn"], mode=Pin.OUT, value=1)
        self.ce = Pin(self.cfg["ce"], mode=Pin.OUT, value=0)
        self.spi = self.cfg["spi"]
        self.nrf = NRF24L01(self.spi, self.csn, self.ce, payload_size=32)

        self.nrf.open_tx_pipe(self.pipes[1])
        self.nrf.open_rx_pipe(1, self.pipes[0])

    def receiver(self):
        self.nrf.start_listening()
        print("NRF24L01 responder mode, waiting for packets...")

        while True:
            # Check if any data is received
            if self.nrf.any():
                # While data has been received
                while self.nrf.any():
                    buf = self.nrf.recv()

                    # Decoding here
                    print("received Message!!")
                    # self.__extractData(buf)
                    
                    self.led.on()

                    utime.sleep_ms(_RX_POLL_DELAY)

                # Give initiator time to get into receive mode.
                utime.sleep_ms(_RESPONDER_SEND_DELAY)

                # Stop boat RF from listening
                self.nrf.stop_listening()

                # Try replying to the message to the initiator
                try:
                    pingMssg = "Got it!"
                    print("sent response: ", pingMssg)
                    self.led.off()
                    self.nrf.send(pingMssg.encode('utf-8'))
                    
                except OSError:
                    print("Cannot send respond!!")
                    pass
                
                # Start listening to RF messages again
                self.nrf.start_listening()

    def nrfReceiverTest(self):
        self.nrf.start_listening()
        print("NRF24L01 responder mode, waiting for packets...")

        while True:
            # Check if any data is received
            if self.nrf.any():
                # While data has been received
                while self.nrf.any():
                    buf = self.nrf.recv()

                    # Decoding here
                    print("received Message!!")     
                    print(buf)
                    pingMssg = str(self.__extractData(buf))
                    self.led.on()
                    utime.sleep_ms(_RX_POLL_DELAY)

                # Give initiator time to get into receive mode.
                utime.sleep_ms(_RESPONDER_SEND_DELAY)

                # Stop boat RF from listening
                self.nrf.stop_listening()

                # Try replying to the message to the initiator
                try:
                    print("sent response: ", pingMssg)
                    self.led.off()
                    self.nrf.send(pingMssg.encode('utf-8'))

                except OSError:
                    print("Cannot send respond!!")
                    pass

                # Start listening to RF messages again
                self.nrf.start_listening()

    def __extractData(self, buf):
        double_identifier = 0x01
        integer_identifier = 0x02

        mssgStartingIndex = 5
        intBufferSize = 4
        doubleBufferSize = 8

        identifier = buf[0]
        dataLength = struct.unpack('i', buf[1:mssgStartingIndex])[0]

        print(dataLength)
        if identifier == double_identifier:
            double_value = struct.unpack('d'* dataLength, buf[mssgStartingIndex:mssgStartingIndex+(doubleBufferSize*dataLength)])
            print(double_value)
            return double_value

        elif identifier == integer_identifier:
            integer_value = struct.unpack('i'* dataLength, buf[mssgStartingIndex:mssgStartingIndex+(intBufferSize*dataLength)])
            print(integer_value)
            return integer_value

        else:
            raise ValueError("Unknown identifier")

         



