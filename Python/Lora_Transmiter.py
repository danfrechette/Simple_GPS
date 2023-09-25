import time
import serial
import RPi.GPIO as GPIO
from argparse import ArgumentParser

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

LSerial = '/dev/ttyS0'
LBaudrate = 9600
LFreqBand = '4330000'
LNetworkID = '7'
LSDevice    = '2'
LDDevice    = '1'

def get_args():
    arg_parser = ArgumentParser(description="Simple LoRa Transmitter.")
    arg_parser.add_argument("-C", required=False, help="Clear Logs", action='store_true')
    arg_parser.add_argument("-serial", required=False, help="Serial", default='/dev/ttyS0')
    arg_parser.add_argument("-baudrate", required=False, help="Baudrate", default='9600')
    arg_parser.add_argument("-frequency", required=False, help="Frequency", default='4330000')
    arg_parser.add_argument("-network", required=False, help="Network ID", default='7')
    arg_parser.add_argument("-pridev", required=False, help="Primary Device", default='2')
    arg_parser.add_argument("-secdev", required=False, help="Secondary Device", default='1')
    args = arg_parser.parse_args()
    return args

def switch1():
    lora.write(b'\x01')

def main():
    global lora
    args = get_args()

    if args.C:
        if os.path.exists(OutputFile): os.remove(OutputFile)
        if os.path.exists(PrevGPSLog): os.remove(PrevGPSLog)

    lora = serial.Serial(LSerial, baudrate= LBaudrate, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
    print(lora)
    time.sleep(1)

    lora.write('AT+BAND={0}'.format(LFreqBand).encode('ascii'))
    lora.write('AT+NETWORKID={0}'.format(LNetworkID).encode('ascii'))
    lora.write('AT+ADDRESS={0}'.format(LDDevice).encode('ascii'))

    print("Aplication Initilized.")
    try:

        print("Start")


        while True:
            lcmd = 'AT+SEND={0},2,{1:.6f}|{2:.6f}'.format(LDDevice,1000,2000).encode('ascii')
            print ("lcmd = " , lcmd)
            lora.write(lcmd)

            #Gets the feedback data and toglle LEDs
            if lora.inWaiting() > 0:
                print("Start")
                data1 = lora.read()
                print(data1)
                switch1()

    except KeyboardInterrupt:
        print ("Exiting Program")
    except Exception as inst :
        print("An error occurred:", type(inst).__name__, ' ', inst)
    finally:
        lora.close()
        pass

if __name__ == "__main__":
    main()


