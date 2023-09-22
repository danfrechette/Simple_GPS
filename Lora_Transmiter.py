#Transmitter code starts here
# https://github.com/chandrawi/LoRaRF-Python
# https://programmaticponderings.com/2020/08/10/lora-and-lorawan-for-iot-getting-started-with-long-range-and-lorawan-specification-for-low-power-wide-area-networking/


import time
import serial
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(12, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(16, GPIO.OUT, initial=GPIO.LOW)

lora = serial.Serial('/dev/ttyAMA0', baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)

time.sleep(1)

relay1 = True
relay2 = True

#Detects button on/off and transmit to LORA
def switch1(ev=None):
    global relay1
    global relay2
    relay1 = not relay1
    if relay1 and relay2:
        lora.write("KEY3")
    elif relay1:
        lora.write("KEY2")
    elif relay2:
        lora.write("KEY1")
    else:
        lora.write("KEY0")

def switch2(ev=None):
    global relay1
    global relay2
    relay2 = not relay2
    if relay1 and relay2:
        lora.write("KEY3")
    elif relay1:
        lora.write("KEY2")
    elif relay2:
        lora.write("KEY1")
    else:
        lora.write("KEY0")

GPIO.add_event_detect(7, GPIO.RISING, callback=switch1, bouncetime=300)
GPIO.add_event_detect(8, GPIO.RISING, callback=switch2, bouncetime=300)

def main():
    try:
        while True:
            #Gets the feedback data and toglle LEDs
            if lora.inWaiting() > 0:
                data1 = lora.read()
                if data1 == 'Y' and lora.inWaiting() > 0:
                    data2 = lora.read()
                    if data2 == 'E' and lora.inWaiting() > 0:
                        data3 = lora.read()
                        if data3 == 'S' and lora.inWaiting() > 0:
                            data4 = lora.read()
                            if data4 == '0':
                                GPIO.output(12, GPIO.HIGH)
                                GPIO.output(16, GPIO.HIGH)
                            elif data4 == '1':
                                GPIO.output(12, GPIO.HIGH)
                                GPIO.output(16, GPIO.LOW)
                            elif data4 == '2':
                                GPIO.output(12, GPIO.LOW)
                                GPIO.output(16, GPIO.HIGH)
                            elif data4 == '3':
                                GPIO.output(12, GPIO.LOW)
                                GPIO.output(16, GPIO.LOW)
    except KeyboardInterrupt:
        print "Exiting Program"
    except:
        print "Error, Exiting Program"
    finally:
        lora.close()
        pass
#Transmitter code ends here

if __name__ == "__main__":
    main()