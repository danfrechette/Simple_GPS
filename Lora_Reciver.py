# https://www.micropeta.com/video7

#Receiver code starts here


import time
import serial
import RPi.GPIO as GPIO
import requests


def Post_GPS_Location (msg: str):
    myobj = {'gps': str}
    x = requests.post("http://localhost:5000", json=myobj)
    print(x.text)




GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(12, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(16, GPIO.OUT, initial=GPIO.HIGH)

lora = serial.Serial('/dev/ttyAMA0', baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
time.sleep(1)

try:
    while True:
        if lora.inWaiting() > 0:
            data1 = lora.read()
            if data1 == 'K' and lora.inWaiting() > 0:
                data2 = lora.read()
                if data2 == 'E' and lora.inWaiting() > 0:
                    data3 = lora.read()
                    if data3 == 'Y' and lora.inWaiting() > 0:
                        data4 = lora.read()
                        if data4 == '0':
                            GPIO.output(12, GPIO.LOW)
                            GPIO.output(16, GPIO.LOW)
                            lora.write("YES0")
                        elif data4 == '1':
                            GPIO.output(12, GPIO.HIGH)
                            GPIO.output(16, GPIO.LOW)
                            lora.write("YES1")
                        elif data4 == '2':
                            GPIO.output(12, GPIO.LOW)
                            GPIO.output(16, GPIO.HIGH)
                            lora.write("YES2")
                        elif data4 == '3':
                            GPIO.output(12, GPIO.HIGH)
                            GPIO.output(16, GPIO.HIGH)
                            lora.write("YES3")
except KeyboardInterrupt:
    print "Exiting Program"
except:
    print "Error, Exiting Program"
finally:
    lora.close()
    pass
#Receiver code ends here