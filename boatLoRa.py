from lib.LoRa.ulora import LoRa, ModemConfig, SPIConfig

class LoRa_TX:
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

    def loraTX(self, data):
        self.lora.send_to_wait(data, self.SERVER_ADDRESS)

class LoRa_RX:
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
        self.lora = LoRa(RFM95_SPIBUS, RFM95_INT, self.SERVER_ADDRESS, RFM95_CS, 
                        reset_pin=RFM95_RST, freq=RF95_FREQ, tx_power=RF95_POW, 
                        acks=True)
    
    def loraRX(self, receivedLoRa):
        # set callback (overwriting exisiting callback)
        self.lora.on_recv = receivedLoRa

        # set to listen continuously
        self.lora.set_mode_rx()

class boatLoRa:
    def __init__(self, brainTX_cb):
        # Callback when wanting to send messages to the brain
        self.brainTX_cb = brainTX_cb

        # Timeout to get ack message from boat
        self.pingTimeout = 0.2

        self.boatLoRa_TX = LoRa_TX()
        self.boatLoRa_RX = LoRa_RX()

        # Initialize interrupt listener for LoRa
        # pass callback function to it
        self.boatLoRa_RX.loraRX(self.rx_cb)

    # LoRa interrupt receiver callback function
    def rx_cb(self, payload):
        if(payload.message[0]==0x21):
            print("Test message from medium!!")
            self.sendMssg('!'.encode())
        else:
            self.sendMssg('!'.encode())
            self.brainTX_cb(payload.message)

    # LoRa sender and wait for acknowledgement
    def sendMssg(self, mssg):
        # Send data through LoRa
        self.boatLoRa_TX.loraTX(mssg)


