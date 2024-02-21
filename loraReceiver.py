import utime
import struct
from lib.LoRa.ulora import LoRa, ModemConfig, SPIConfig

class boatLoRa:
    def __init__(self):
        # for debugging purposes during testing
        self.counter = 0

        # Lora Parameters
        RFM95_RST = 3
        RFM95_SPIBUS = SPIConfig.rp2_0
        RFM95_CS = 5
        RFM95_INT = 2
        RF95_FREQ = 433.0
        RF95_POW = 20
        self.CLIENT_ADDRESS = 253
        self.SERVER_ADDRESS = 199

        # initialise radio
        self.lora = LoRa(RFM95_SPIBUS, RFM95_INT, self.SERVER_ADDRESS, RFM95_CS, reset_pin=RFM95_RST, freq=RF95_FREQ, tx_power=RF95_POW, acks=True)

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
            return double_value

        elif identifier == integer_identifier:
            integer_value = struct.unpack('i'* dataLength, buf[mssgStartingIndex:mssgStartingIndex+(intBufferSize*dataLength)])
            return integer_value

        else:
            raise ValueError("Unknown identifier")
        
    def testCallback(self, payload):
        self.counter = self.counter + 1
        print("******************************************")
        print("From:", payload.header_from)
        print("Message No.",self.counter)
        print("Received:", self.__extractData(payload.message))
        print("RSSI: {}; SNR: {}".format(payload.rssi, payload.snr))
        pass

    def loraReceiverTest(self):
        # set callback (overwriting exisiting callback)
        self.lora.on_recv = self.testCallback

        # set to listen continuously
        self.lora.set_mode_rx()

        # loop and wait for data
        while True:
            utime.sleep_ms(10)

# # This is our callback function that runs when a message is received
# def on_recv(payload):
#     print("From:", payload.header_from)
#     print("Received:", payload.message)
#     print("RSSI: {}; SNR: {}".format(payload.rssi, payload.snr))

