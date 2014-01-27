import serial
import time

import numpy as np
from scipy.interpolate import spline
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema

from scipy.interpolate import UnivariateSpline
from scipy.signal import wiener, filtfilt, butter, gaussian, freqz
from scipy.ndimage import filters
import scipy.optimize as op

from threading import *

import sys
sys.path.append("/Users/nahiyanmalik/Development/wxPython-src-3.0.0.0/wxPython")

import wx
import gui

stdThresholdLow = 15;
stdThresholdHigh = 400;

def arduinoRead():
    while True:
        time.sleep(2)

        t, v = [], []
        data = arduino.read(arduino.inWaiting())
        sample = data.split('\n')
        del sample[-1]

        for line in sample:
        	values = line.split()
        	values = map(int, values)

        	# print "SIZE: ", len(values)

        	# print "t val 0: ", values[0]
        	# print "v val 1: ", values[1]        	

        	# append if there are both values, otherwise it breaks
        	if len(values) == 2:
	        	t.append(values[0])
	        	v.append(values[1])

        	# if values[0] and values[1]:
        	# 	t.append(values[0])
        	# 	v.append(values[1])

        vSmooth = gaussSmooth(v);

        # print v
        # print vSmooth

        # print "v size and type: ", len(v), type(v)
        # print "vSmooth size and type: ", len(vSmooth), type(vSmooth)

        # vNp = np.array(v)

        # maximaV = argrelextrema(vNp, np.greater)
        # print maximaV

        # customMaximaV = maxima(v)
        # print customMaximaV

        smoothMaxima = maxima(vSmooth)
        # print smoothMaxima

        bpm, ibi = sampleStats(smoothMaxima, t)

        vStd = np.std(v)
        # print "standard deviation: ", vStd
        status = 0 #0: not a good pulse. 1: good pulse.

        if vStd > stdThresholdLow and vStd < stdThresholdHigh and bpm > 20 and ibi < 3000:
        	status = 1

        print "SAMPLE BPM: ", bpm
        print "PULSE STATUS: ", status

        epochTime = time.time()

        fullStats[0].append(t[-1])
        fullStats[1].append(epochTime)
        fullStats[2].append(bpm)
        fullStats[3].append(ibi)
        fullStats[4].append(status)

        # print fullStats

        writeFile.write(str(t[-1]) + "\t" + str(epochTime) + "\t" + str(bpm) + "\t" + str(ibi) + "\t" + str(status) + "\n");

        #RUN STUFF NOW

def calibrate():
    statusCount = 0

    while True:
        time.sleep(2)

        t, v = [], []
        data = arduino.read(arduino.inWaiting())
        sample = data.split('\n')
        del sample[-1]

        for line in sample:
            values = line.split()
            values = map(int, values)

            # append if there are both values, otherwise it breaks
            if len(values) == 2:
                t.append(values[0])
                v.append(values[1])

        vSmooth = gaussSmooth(v);

        smoothMaxima = maxima(vSmooth)

        bpm, ibi = sampleStats(smoothMaxima, t)

        vStd = np.std(v)

        status = 0 #0: not a good pulse. 1: good pulse.
        stdThresholdLow = 25;
        stdThresholdHigh = 400;

        if vStd > stdThresholdLow and vStd < stdThresholdHigh and bpm > 20 and ibi < 3000:
            status = 1
            statusCount += 1
        else:
            statusCount = 0

        if statusCount == 10:
            return 1

        print status


def maxima(vals):
	size = len(vals)
	maxVals = []
	lastVal = 0
	currVal = 0
	incr = 0 # 0 is decr (default), 1 is incr, 2 is flat (currently just using 1)
	flat = 0

	for i in range(size):
		currVal = vals[i]

		if i != 0:
			lastVal = vals[i-1]
			currVal = vals[i]
			rate = currVal - lastVal
			localIncr = 0

			if rate == 0:
				flat = 1
			elif rate < 0:
				localIncr = 0
				flat = 0
			elif rate > 0:
				flat = 0
				localIncr = 1

			if localIncr == 0 and incr == 1 and flat == 0:
				maxVals.append(i-1)
				incr = localIncr
			elif localIncr == 0 and incr == 1 and flat == 1:
				incr = incr
			else:
				incr = localIncr

	return maxVals

def gaussSmooth(vals):
	b = gaussian(50, 2)
	smoothVals = filters.convolve1d(vals, b/b.sum())
	return smoothVals

def sampleStats(maximaIndexes, times):
	noPeaks = len(maximaIndexes)
	IBIs = []
	avgIBI = 0
	avgBPM = 0

	for i in range(noPeaks):
		if i != 0:
			ibi = times[maximaIndexes[i]] - times[maximaIndexes[i-1]]
			IBIs.append(ibi)

	avgIBI = np.mean(IBIs)
	avgBPM = 60000/avgIBI

	# print "IBIs: ", IBIs

	# print "AVERAGE IBI: ", avgIBI

	return (avgBPM, avgIBI)

class CalibrateEvent(wx.PyEvent):
    def __init__(self, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(gui.EVT_CALIBRATE_ID)
        self.data = data

class CalibrateThread(Thread):
    def __init__(self, notify_window):
        Thread.__init__(self)
        self._notify_window = notify_window
        self._want_abort = 0
        self.start()

    def run(self):
        arduino = serial.Serial('/dev/tty.usbmodem1421',115200)
        fullStats = [[],[],[],[],[]] #cols: run time, epoch time, bpm, ibi, status (0 no pulse, 1 pulse)
        writeFile = open( 'writefile.txt', 'w' )
        statusCount = 0

        while True:
            
            print "abort value: ", self._want_abort

            if self._want_abort == 1:
                arduino.close()
                self._want_abort = 0
                break

            time.sleep(2)

            t, v = [], []
            data = arduino.read(arduino.inWaiting())
            sample = data.split('\n')
            del sample[-1]

            for line in sample:
                values = line.split()
                values = map(int, values)

                # append if there are both values, otherwise it breaks
                if len(values) == 2:
                    t.append(values[0])
                    v.append(values[1])

            vSmooth = gaussSmooth(v);

            smoothMaxima = maxima(vSmooth)

            bpm, ibi = sampleStats(smoothMaxima, t)

            vStd = np.std(v)

            status = 0 #0: not a good pulse. 1: good pulse.
            

            if vStd > stdThresholdLow and vStd < stdThresholdHigh and bpm > 20 and ibi < 3000:
                status = 1
                statusCount += 1
            else:
                statusCount = 0

            if statusCount == 10:
                wx.PostEvent(self._notify_window, CalibrateEvent(1))
                arduino.close()
                gui.worker = None
                return

            print status
            print vStd
            print bpm
            print ibi           

    def abort(self):
        self._want_abort = 1

class ResultEvent(wx.PyEvent):
    def __init__(self, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(gui.EVT_RESULT_ID)
        self.data = data

class BPMThread(Thread):
    def __init__(self, notify_window):
        Thread.__init__(self)
        self._notify_window = notify_window
        self._want_abort = 0
        self.start()

    def run(self):
        arduino = serial.Serial('/dev/tty.usbmodem1421',115200)
        fullStats = [[],[],[],[],[]] #cols: run time, epoch time, bpm, ibi, status (0 no pulse, 1 pulse)
        writeFile = open( 'writefile.txt', 'w' )

        firstEpoch = 0

        while True:

            print "abort value: ", self._want_abort

            if self._want_abort == 1:
                arduino.close()
                self._want_abort = 0
                break

            time.sleep(2)

            t, v = [], []
            data = arduino.read(arduino.inWaiting())
            sample = data.split('\n')
            del sample[-1]

            for line in sample:
                values = line.split()
                values = map(int, values)

                # print "SIZE: ", len(values)

                # print "t val 0: ", values[0]
                # print "v val 1: ", values[1]          

                # append if there are both values, otherwise it breaks
                if len(values) == 2:
                    t.append(values[0])
                    v.append(values[1])

                # if values[0] and values[1]:
                #   t.append(values[0])
                #   v.append(values[1])

            vSmooth = gaussSmooth(v);

            # print v
            # print vSmooth

            # print "v size and type: ", len(v), type(v)
            # print "vSmooth size and type: ", len(vSmooth), type(vSmooth)

            # vNp = np.array(v)

            # maximaV = argrelextrema(vNp, np.greater)
            # print maximaV

            # customMaximaV = maxima(v)
            # print customMaximaV

            smoothMaxima = maxima(vSmooth)
            # print smoothMaxima

            bpm, ibi = sampleStats(smoothMaxima, t)

            vStd = np.std(v)
            # print "standard deviation: ", vStd
            status = 0 #0: not a good pulse. 1: good pulse.
            stdThresholdLow = 25;
            stdThresholdHigh = 400;

            if vStd > stdThresholdLow and vStd < stdThresholdHigh and bpm > 20 and ibi < 3000:
                status = 1

            print "SAMPLE BPM: ", bpm
            print "PULSE STATUS: ", status

            epochTime = time.time()

            # if firstEpoch == 0:
            #     firstEpoch = epochTime



            fullStats[0].append(t[-1])
            fullStats[1].append(epochTime)

            fullStats[2].append(bpm)
            fullStats[3].append(ibi)
            fullStats[4].append(status)

            # print fullStats

            writeFile.write(str(t[-1]) + "\t" + str(epochTime) + "\t" + str(bpm) + "\t" + str(ibi) + "\t" + str(status) + "\n");

            wx.PostEvent(self._notify_window, ResultEvent((str(bpm),str(ibi))))

    def abort(self):
        self._want_abort = 1


def bpmRun():
    arduino = serial.Serial('/dev/tty.usbmodem1421',115200)
    fullStats = [[],[],[],[],[]] #cols: run time, epoch time, bpm, ibi, status (0 no pulse, 1 pulse)
    writeFile = open( 'writefile.txt', 'w' )
    calibrate()

if __name__ == '__main__':
    print "HERERERERER"
    bpmRun()    


#HAVE TO IMPLEMENT STD TO MAKE SURE THAT THERE IS CHANGE.
#EX. IF STD IS 1-5, NO PULSE LETS SAY
