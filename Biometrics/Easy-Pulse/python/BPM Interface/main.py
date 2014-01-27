import sys
sys.path.append("/Users/nahiyanmalik/Development/wxPython-src-3.0.0.0/wxPython")

import wx
import gui
import processing
import functions

import serial
import time
import datetime
import re

from threading import *
 
class MainApp(gui.RealtimeInterface):
    # def OnInit(self):
    #     frame = gui.RealtimeInterface(None)
    #     frame.Show(True)
    #     self.SetTopWindow(frame)
    #     self.frame = frame
    #     return True


    def OnInit(self, parent):
        gui.RealtimeInterface.__init__(self, parent)

    def CloseTread(self, parent):
        self.worker = None
        processing.arduino.close()

    def bpmResult(self, event):
        self.bpmValue.SetLabel(event.data[0])
        self.ibiValue.SetLabel(event.data[1])

    def bpmStart(self, event):
        if not self.worker:
            self.worker = processing.BPMThread(self)
            self.bpmButton.SetLabel("Stop")
        else:
            self.worker.abort()
            self.worker = None
            self.bpmButton.Enable(False)

    def calibrate(self, event):
        if not self.worker:
            self.worker = processing.CalibrateThread(self)
            self.calibrateButton.SetLabel("Calibrating / Click to Stop")
        else:
            self.worker.abort()
            self.worker = None
            self.calibrateButton.SetLabel("Calibrate")

    def calibrateResult(self, event):
        if event.data == 1:
            self.worker = None
            print "calibrated"
            print "min: ", processing.getCalibrateLow()
            print "max: ", processing.getCalibrateHigh()
            print "mean: ", processing.getCalibrateMean()

            self.calibrateButton.Enable(False)
            self.calibrateButton.SetLabel("Calibrated")
            self.patientChoice.Enable(True)
            self.bpmButton.Enable(True)
        else:
            print "not calibrated"
            self.worker = None
        return



def main():
    app = wx.App()
    window = MainApp(None)
    window.Show(True)
    app.MainLoop()

if __name__ == '__main__':
    main()