import re
import time
import random
from itertools import cycle

##import gps
##import serial
##import subprocess

colors = ['black','red','yellow','green','blue']
colors_cycle = cycle(colors)

def next_color():
    return next(colors_cycle)

def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs: setattr(func, k, kwargs[k])
        return func
    return decorate

@static_vars(Lat=0, Lng =0)
def PrevGPS(Lat, Lng):
     ret = False

     if abs(PrevGPS.Lat - Lat) >= 10 or abs(PrevGPS.Lng - Lng) >= 10:
        print('Last Lat:\t {0} , Lng: {1}'.format(PrevGPS.Lat, PrevGPS.Lng ))
        PrevGPS.Lat = Lat
        PrevGPS.Lng = Lng
        ret = True

     if ret: print('New Lat:\t {0} , Lng: {1}'.format(PrevGPS.Lat, PrevGPS.Lng ))
     return ret

def readGPSdata():#ser):
    while True:
        ## reading = ser.readline().decode('utf-8')
        readings = ['$GPGLL,4249.76150,N,08316.47059,W,101745.00,A,A*70',
                    '$GPGLL,4249.76150,N,08316.47059,W,101745.00,A,A*70',
                    '$GPGLL,4249.76150,N,08316.47059,W,101745.00,A,A*70',
                    '$GPGLL,4249.76150,N,08316.47059,W,101745.00,A,A*70',
                    '$GPGLL,4249.76150,N,08316.47059,W,101745.00,A,A*70',
                    '$GPGLL,4249.76150,N,08316.47059,W,101745.00,A,A*70',
                    '$GPGLL,4249.76150,N,08316.47059,W,101745.00,A,A*70',
                    '$GPGLL,4249.76155,N,08316.47060,W,101745.00,A,A*70',
                    '$GPGLL,4249.76160,N,08316.47069,W,101750.00,A,A*70',
                    '$GPGLL,4249.76165,N,08316.47079,W,101755.00,A,A*70']

        reading = random.choice(readings)
        if reading:
            #print(reading)
            evalGPSdata(reading)

def evalGPSdata(reading):
    regex = r'\$GPGLL.*,(\d+)(\d{2,2}[\.]\d+),([N]),(\d+)(\d{2,2}[\.]\d+),([W])'
    eval = re.findall(regex,reading)
    if len(eval) > 0:
        latdgr, latmin, latdir, lngdgr, lngmin, lngdir = eval[0]

        evalLat = int((float(latmin) % 1) * 100000)
        evalLng = int((float(lngmin) % 1) * 100000)
        if PrevGPS(evalLat, evalLng):
            calcGPSdata(latdgr, latmin, latdir, lngdgr, lngmin, lngdir)
        time.sleep(1)

def calcGPSdata(latdgr, latmin, latdir, lngdgr, lngmin, lngdir):
     Lat = float(latdgr) + (float(latmin) / 60.0)
     Lng = float(lngdgr) + (float(lngmin) / 60.0)

     if(latdir == 'S'): Lat = Lat * -1
     if(lngdir == 'W'): Lng = Lng * -1

     print('Lat: {0:.6f} , Lon: {1:.6f}\n'.format(Lat, Lng ))
     recGPSdata(Lat, Lng)


def recGPSdata(Lat, Lng):
    strOutput = '{0:.5f},{1:.5f},{2},circle,""\n'.format(Lat, Lng, next_color())
    print(strOutput)

#    with open("gpsLog.txt", "a") as file1:
#       file1.write(strOutput)

    time.sleep(1)

SERIAL_PORT = '/dev/ttyUSB0'
# this port address is for the serial tx/rx pins on the GPIO header
SERIAL_RATE = 9600
# be sure to set this to the same rate used on the Arduino

def main():
    try:
        print("Main try:")
        ## ser = serial.Serial(SERIAL_PORT, SERIAL_RATE)
        readGPSdata()## ser)
    except:
        #print("An error occurred:", type(error).__name__, "–", error)
        print("Main Except:")
        #  proc1 = subprocess.Popen(['lsmod'], stdout=subprocess.PIPE)
        #  proc2 = subprocess.Popen(['grep', 'usbserial'], stdin=proc1.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #  proc1.stdout.close() # Allow proc1 to receive a SIGPIPE if proc2 exits.
        #  out, err = proc2.communicate()
        #
        #  print('Out: {0}'.format(out))
        #
        #  regex = r'^(.*?\d?)(\w+)[\\].*$'
        #  eval = re.findall(regex, str(out))
        #  if len(eval) > 0:
        #
        #      usbPort = str(eval[0][1])
        #
        #      #sudo modprobe -r ftdi_sio
        #      #sudo modprobe -r usbserial
        #
        #      #subprocess.run([], stdout=subprocess.PIPE)
        #      args = ['sudo','modprobe', '-r' , usbPort]
        #      proc1 = subprocess.Popen(args, stdout=subprocess.PIPE)
        #      #proc2 = subprocess.Popen(['modprobe', '-r ' + usbPort], stdin=proc1.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #      proc1.stdout.close() # Allow proc1 to receive a SIGPIPE if proc2 exits.
        #      #out, err = proc2.communicate()
        #
        #      #print ("OUT:" + out)
        time.sleep(5)
        ## main()
if __name__ == "__main__":
    main()