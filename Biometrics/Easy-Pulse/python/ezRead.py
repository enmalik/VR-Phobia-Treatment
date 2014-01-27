import serial
import time
import datetime
import re


def receiving(ser):
    # regex = re.compile("[.*]_")
    while True:
        time.sleep(2)
        read = ser.read(ser.inWaiting())
        print read

        #RUN STUFF NOW

arduino = serial.Serial('/dev/tty.usbmodem1421',115200)
receiving(arduino);
