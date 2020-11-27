import RPi.GPIO as GPIO
from gpiozero import Servo
from pn532 import *
import time
import datetime


if __name__ == '__main__':
    try:
        #pn532 = PN532_SPI(debug=False, reset=20, cs=4)
        #pn532 = PN532_I2C(debug=False, reset=20, req=16)
        pn532 = PN532_UART(debug=False, reset=20)
        
        servo = Servo(6)
        servo.min()
        ic, ver, rev, support = pn532.get_firmware_version()
        print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))
        kode=[]
        key =[]
        # Configure PN532 to communicate with MiFare cards
        pn532.SAM_configuration()
        #i=hex  
        print('Waiting for RFID/NFC card...')
        while True:
            # Check if a card is available to read
            uid = pn532.read_passive_target(timeout=0.5)
            print('.', end="")
            servo.min()
            # Try again if no card is available.
            if uid is None:
                continue
             
            kode =[hex(i) for i in uid]
            key = ['0x1', '0x23', '0x45', '0x67']
            #print('Found card with UID:', kode)
            #timeout =2
            if key == kode:
                print('OK')
                f=open('text.txt','a')
                f.write("open ")
                f.write(datetime.datetime.now().ctime()+'\n')
                f.close()
                servo.max()
                time.sleep(3)
                servo.min()
                time.sleep(3)
            else:
                print('False')
                f=open('text.txt','a')
                f.write("access denied ")
                f.write(datetime.datetime.now().ctime()+'\n')
                f.close()
                servo.min()
                time.sleep(3)
                
    except Exception as e:
        print(e)
    finally:
        GPIO.cleanup()
