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

import wx
import gui
import functions
import os

# arduinoPort = "COM3" #nahiyan
# arduinoPort = "COM6" #bala
arduinoPort = "/dev/tty.usbmodem1421"

smoothStd = 4
bpmThreshold = 140

stdThresholdLow = 5
stdThresholdHigh = 500

calibrateLow = 0
calibrateHigh = 0
calibrateMean = 0

plotValidation = False

# delay increment in ms. (samplerate in / number of values)
# delayIncrement = 25 # currently synced with arduino. DO NOT CHANGE EITHER.

delayIncrement = 0

# sample delay in seconds
sampleDelay = 5.0

sessionDir = ""

def getSessionDir():
    return str(sessionDir)

def setSessionDir(newID):
    global sessionDir
    sessionDir = newID

def getCalibrateLow():
    return calibrateLow

def getCalibrateHigh():
    return calibrateHigh

def getCalibrateMean():
    return calibrateMean

def arduinoRead():
    while True:
        time.sleep(sampleDelay)

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
        time.sleep(sampleDelay)

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
    global smoothStd
    numVals = len(vals)

    if numVals == 0:
        numVals = 1

    print "number of values: ", numVals

    print type(vals)
    print "########VALUES#########\n", vals

    b = gaussian(numVals, smoothStd)
    smoothVals = filters.convolve1d(vals, b/b.sum())
    
    print type(smoothVals)
    print "########SMOOTH VALUES#########\n", list(smoothVals)

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
        arduino = serial.Serial(arduinoPort,115200)

        statusCount = 0
        calibrateBPM = []

        numArduinoResults = []
        maxCounter = 0

        # to get correct increment
        while True:
            print "In max value calibration"

            print "abort value: ", self._want_abort

            if self._want_abort == 1:
                arduino.close()
                # don't reset to 0 because there's the other while loop after this for bpm calibration
                break

            maxCounter += 1

            time.sleep(sampleDelay)

            data = arduino.read(arduino.inWaiting())
            sample = data.split('\n')

            numLine = 0

            for line in sample:
                numLine += 1

            numArduinoResults.append(numLine)

            print numLine

            if maxCounter == 5:
                print numArduinoResults
                maxNumVals = np.max(numArduinoResults)
                global delayIncrement
                delayIncrement = (sampleDelay * 1000) / maxNumVals

                print "delay increment: ", delayIncrement

                # arduino.close()
                break



        while True:
            "In BPM calibration"

            print "abort value: ", self._want_abort

            if self._want_abort == 1:
                arduino.close()
                self._want_abort = 0
                break

            time.sleep(sampleDelay)

            t, v = [], []

            data = arduino.read(arduino.inWaiting())
            sample = data.split('\n')
            del sample[-1]

            # Increment should be the same as the delay in the Arduino code
            delayInterval = 0

            for line in sample:
                delayInterval += delayIncrement
                # print "Arduino Values: ", line

                try:
                    t.append(delayInterval)
                    v.append(int(line))
                except:
                    print "EMPTY RETURN FROM ARDUINO - IGNORING IT!"
                    continue


            vSmooth = gaussSmooth(v);

            smoothMaxima = maxima(vSmooth)

            bpm, ibi = sampleStats(smoothMaxima, t)

            vStd = np.std(v)

            status = 0 #0: not a good pulse. 1: good pulse.

            print "TYPE: ", type(bpm)
            calibrateBPM.append(bpm)
            
            if vStd > stdThresholdLow and vStd < stdThresholdHigh and bpm > 20 and ibi < 3000:
                status = 1
                statusCount += 1
            else:
                status = 0
                statusCount = 0

            global smoothStd
            global bpmThreshold

            if bpm > bpmThreshold and smoothStd < 5:
                print "incrementing smooth std from ", smoothStd, " to ", smoothStd + 1
                smoothStd += 1
                status = 0
                statusCount = 0

            # if statusCount == 15:
            #     global calibrateLow, calibrateHigh, calibrateMean

            #     calibrateLow = np.min(calibrateBPM[-10:-1])
            #     calibrateHigh = np.max(calibrateBPM[-10:-1])
            #     calibrateMean = np.mean(calibrateBPM[-10:-1])

            #     print "min: ", calibrateLow
            #     print "max: ", calibrateHigh
            #     print "mean: ", calibrateMean

            #     wx.PostEvent(self._notify_window, CalibrateEvent(1))
            #     arduino.close()

            #     gui.worker = None
            #     return

            #for demo calibration set to 6
            if statusCount == 6:
                global calibrateLow, calibrateHigh, calibrateMean

                calibrateLow = np.min(calibrateBPM[-4:-1])
                calibrateHigh = np.max(calibrateBPM[-4:-1])
                calibrateMean = np.mean(calibrateBPM[-4:-1])

                print "min: ", calibrateLow
                print "max: ", calibrateHigh
                print "mean: ", calibrateMean

                wx.PostEvent(self._notify_window, CalibrateEvent(1))
                arduino.close()

                gui.worker = None
                return

            print "STATUS: ", status
            print "STD: ", vStd
            print "BPM: ", bpm
            print "IBI: ", ibi           

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
        arduino = serial.Serial(arduinoPort,115200)
        fullStats = [[],[],[],[],[], []] #cols: run time, epoch time, bpm, ibi, status (0 no pulse, 1 pulse)
        print getSessionDir() + 'data.txt' 
        writeFile = open( getSessionDir() + 'data.txt', 'w' )

        # skip the first read to avoid ridiculous values
        firstRead = True

        # first epoch time
        firstEpoch = 0

        while True:
            print "abort value: ", self._want_abort

            if self._want_abort == 1:
                arduino.close()
                writeFile.close()
                global plotValidation
                plotValidation = functions.singleRunPlot(getSessionDir(), getSessionDir() + 'data.txt', getCalibrateLow(), getCalibrateHigh(), getCalibrateMean())
                self._want_abort = 0
                print plotValidation
                break

            time.sleep(sampleDelay)

            t, v = [], []
            data = arduino.read(arduino.inWaiting())
            sample = data.split('\n')
            del sample[-1]

            numIssues = 0

            # Increment should be the same as the delay in the Arduino code
            delayInterval = 0

            for line in sample:
                delayInterval += delayIncrement
                print "Arduino Values: ", line

                try:
                    t.append(delayInterval)
                    v.append(int(line))
                except:
                    print "EMPTY RETURN FROM ARDUINO - IGNORING IT!"
                    numIssues += 1
                    continue


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

            if firstRead == True:
                bpm = getCalibrateMean()
                ibi = 60000/bpm
                firstRead = False
            else:
                bpm, ibi = sampleStats(smoothMaxima, t)

            vStd = np.std(v)
            # print "standard deviation: ", vStd
            status = 0 #0: not a good pulse. 1: good pulse.

            if vStd > stdThresholdLow and vStd < stdThresholdHigh and bpm > 20 and ibi < 3000:
                status = 1

            print "SAMPLE BPM: ", bpm
            print "PULSE STATUS: ", status

            epochTime = time.time()

            if firstEpoch == 0:
                firstEpoch = epochTime

            epochDiff = int(epochTime - firstEpoch)



            fullStats[0].append(t[-1])
            fullStats[1].append(epochTime)
            fullStats[2].append(epochDiff)
            fullStats[3].append(bpm)
            fullStats[4].append(ibi)
            fullStats[5].append(status)

            # print fullStats

            writeFile.write(str(t[-1]) + "\t" + str(epochTime) + "\t" + str(epochDiff) + "\t" + str(bpm) + "\t" + str(ibi) + "\t" + str(status) + "\n");

            wx.PostEvent(self._notify_window, ResultEvent((str(bpm),str(ibi))))

            # Restart Arduino if there are more than 5 empty returns
            if numIssues > 4:
                arduino.close()
                time.sleep(2)
                arduino = serial.Serial(arduinoPort,115200)
                time.sleep(2)

    def abort(self):
        self._want_abort = 1


# def bpmRun():
#     arduino = serial.Serial(arduinoPort,115200)
#     fullStats = [[],[],[],[],[], []] #cols: run time, epoch time, bpm, ibi, status (0 no pulse, 1 pulse)
#     writeFile = open( 'writefile.txt', 'w' )
#     BPMThread(self)

# if __name__ == '__main__':
#     print "HERERERERER"
#     bpmRun()    


#HAVE TO IMPLEMENT STD TO MAKE SURE THAT THERE IS CHANGE.
#EX. IF STD IS 1-5, NO PULSE LETS SAY
