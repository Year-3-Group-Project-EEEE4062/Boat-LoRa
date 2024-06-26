from machine import Pin, UART
import sys
import select
import ubinascii
from boatLoRa import boatLoRa

def main():
    # Setup on board LED to let user know also if BLE connected or not 
    led = Pin("LED", Pin.OUT)
    led.off()

    # Set up the poll object
    poll_obj = select.poll()
    poll_obj.register(sys.stdin, select.POLLIN)

    ##################################################################
    ## main operation
    while True:
        try:
            LoRa = boatLoRa()
            break
        except:
            print("LoRa init error!")

    led.on() # Indicate everything initialized

    while True:        
        # Wait for input on stdin
        poll_results = poll_obj.poll(1) # the '1' is how long it will wait for message before looping again (in microseconds)
        
        if poll_results:
            try:
                base64_str = sys.stdin.readline().strip()
                reply = bytearray(ubinascii.a2b_base64(base64_str))
                LoRa.sendMssg(reply)
            except:
                print("Cannot!!")

if __name__=="__main__":
    try:
        main()
    except Exception as e:
        print(e)

