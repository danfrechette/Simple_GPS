import re
import time
import random
from itertools import cycle
import gps
import serial
import subprocess

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
     tol = 1
     if abs(PrevGPS.Lat - Lat) >= tol or abs(PrevGPS.Lng - Lng) >= tol:
        PrevGPS.Lat = Lat
        PrevGPS.Lng = Lng
        ret = True

     return ret

def readGPSdata(ser):
    while True:
        reading = ser.readline().decode('utf-8')
        if reading:
            evalGPSdata(reading)

def evalGPSdata(reading):
    regex = r'\$GPGLL.*,(\d+)(\d{2,2}[\.]\d+),([N]),(\d+)(\d{2,2}[\.]\d+),([W])'
    eval = re.findall(regex,reading)
    if len(eval) > 0:
        latdgr, latmin, latdir, lngdgr, lngmin, lngdir = eval[0]

        Lat, Lng = calcGPSdata(latdgr, latmin, latdir, lngdgr, lngmin, lngdir)

        evalLat = int((Lat % 1) * 100000)
        evalLng = int((Lng % 1) * 100000)

        if PrevGPS(evalLat, evalLng):
            recGPSdata(Lat, Lng)

def calcGPSdata(latdgr, latmin, latdir, lngdgr, lngmin, lngdir):
     Lat = float(latdgr) + (float(latmin) / 60.0)
     Lng = float(lngdgr) + (float(lngmin) / 60.0)

     if(latdir == 'S'): Lat = Lat * -1
     if(lngdir == 'W'): Lng = Lng * -1

     return Lat, Lng


def recGPSdata(Lat, Lng):
    strOutput = '{0:.6f},{1:.6f},{2},circle,""'.format(Lat, Lng, next_color())
    with open("gpsLog.txt", "a") as file1:
       file1.write(strOutput + '\n')

SERIAL_PORT = '/dev/ttyUSB0'
SERIAL_RATE = 9600

def main():
    try:
        ser = serial.Serial(SERIAL_PORT, SERIAL_RATE)
        readGPSdata(ser)
    except Exception as inst :
        print("An error occurred:", type(inst).__name__, '–', inst)
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