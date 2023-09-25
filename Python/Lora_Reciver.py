import time
import serial
import RPi.GPIO as GPIO
import requests
from argparse import ArgumentParser

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
    arg_parser.add_argument("-pridev", required=False, help="Primary Device", default='1')
    arg_parser.add_argument("-secdev", required=False, help="Secondary Device", default='2')
    args = arg_parser.parse_args()
    return args

def Post_GPS_Location (msg: str):
    myobj = {'gps': str}
    x = requests.post("http://localhost:5000", json=myobj)
    print(x.text)

def main():
    args = get_args()

    if args.C:
        if os.path.exists(OutputFile): os.remove(OutputFile)
        if os.path.exists(PrevGPSLog): os.remove(PrevGPSLog)

    try:
        lora = serial.Serial(LSerial, baudrate= LBaudrate, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
        time.sleep(1)

        lora.write('AT+BAND={0}'.format(LFreqBand).encode('ascii'))
        lora.write('AT+NETWORKID={0}'.format(LNetworkID).encode('ascii'))
        lora.write('AT+ADDRESS={0}'.format(LDDevice).encode('ascii'))

        print("Aplication Initilized.")

        while True:
            if lora.inWaiting() > 0:
                print("reading.")
                data1 = lora.read(10)
                print(data1)

                if data1 == 'K' and lora.inWaiting() > 0:
                    data2 = lora.read()
                    data3 = lora.read()
                    data4 = lora.read()

    except KeyboardInterrupt:
        print("Exiting Program")
    except:
        print("Error, Exiting Program")
    finally:
        lora.close()
        pass

if __name__ == "__main__":
    main()
