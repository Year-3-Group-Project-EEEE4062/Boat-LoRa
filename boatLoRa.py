import utime
import struct
from lib.LoRa.ulora import LoRa, ModemConfig, SPIConfig

class boatLoRa_TX:
    def __init__(self):
    # Lora Parameters
        RFM95_RST = 19 # RST GPIO Pin
        RFM95_SPIBUS = SPIConfig.tx # SPI0
        RFM95_CS = 1 # NSS GPIO Pin
        RFM95_INT = 18 # Interrupt GPIO Pin (DIO0)
        RF95_FREQ = 433.0
        RF95_POW = 20
        self.CLIENT_ADDRESS = 253
        self.SERVER_ADDRESS = 199

        # initialise radio
        self.lora = LoRa(RFM95_SPIBUS, RFM95_INT, self.CLIENT_ADDRESS, RFM95_CS,
                     reset_pin=RFM95_RST, freq=RF95_FREQ, tx_power=RF95_POW, 
                     acks=True)

    def __doubleTest(self):
        # Can only send a maximum of 4 doubles per transmission
        dataToBeSent = [2.9438889,101.8735556]
        double_identifier = 0x01

        data = bytearray()
        data.extend(double_identifier.to_bytes(1,'big')) # data type identifier
        data.extend(struct.pack('i', len(dataToBeSent))) # how many data to extracted
        data.extend(struct.pack('d' * len(dataToBeSent), *dataToBeSent)) # the data itself

        print(data)
        return data

    def loraSenderTest(self):
        counter = 0

        while True:
            # get practice message
            data = self.__doubleTest()
            self.lora.send_to_wait(data, self.SERVER_ADDRESS)
            print("Data type: ", type(data))
            counter = counter + 1
            print("sent LoRa message No.",counter,"!")
            utime.sleep_ms(500)

class boatLoRa_RX:
    def __init__(self):
        # for debugging purposes during testing
        self.counter = 0

        # Lora Parameters
        RFM95_RST = 17 # RST pin
        RFM95_SPIBUS = SPIConfig.rx
        RFM95_CS = 5 # NSS pin 
        RFM95_INT = 16 #DIO0 pin
        RF95_FREQ = 433.0
        RF95_POW = 20
        self.CLIENT_ADDRESS = 243
        self.SERVER_ADDRESS = 189

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

