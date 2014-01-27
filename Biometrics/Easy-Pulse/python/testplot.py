import serial
import time


import numpy as np
from matplotlib import pyplot as plt
ser = serial.Serial('/dev/tty.usbmodem1421',115200)
 
plt.ion() # set plot to animated
 
ydata = [0] * 50
ax1=plt.axes()  
 
# make plot
line, = plt.plot(ydata)
plt.ylim([10,40])
 
# start data collection
while True:
    time.sleep(0.05)  
    data = ser.readline().rstrip() # read data from serial 
                                   # port and strip line endings
    ydata.append(data)
    line.set_xdata(np.arange(len(ydata)))
    line.set_ydata(ydata)  # update the data
    plt.draw() # update the plot