import wx
import gui
import processing
import functions
import os
import shutil

import serial
import time
import datetime
import re

from threading import *

cwd = os.getcwd()
workingDir = cwd + "/App/"

# workingDir = "/Users/nahiyanmalik/Dropbox/FYDP/Windows/RT Biometrics/App/"
# workingDir = "C:/Users/NM/Dropbox/FYDP/Windows/RT Biometrics/App/"

sessionDir = workingDir + "/Sessions/"

prevDir = os.path.abspath('..')
piDir = prevDir + "/Psychologist Interface/App/"

# piDir = "/Users/nahiyanmalik/Dropbox/FYDP/Windows/Psychologist Interface/App/"
# piDir = "C:/Users/NM/Dropbox/FYDP/Windows/Psychologist Interface/App/"

piPatientsDir = piDir + "/Patients/"


class MainApp(gui.RealtimeInterface):
    # def OnInit(self):
    #     frame = gui.RealtimeInterface(None)
    #     frame.Show(True)
    #     self.SetTopWindow(frame)
    #     self.frame = frame
    #     return True


    def __init__(self, parent):
        gui.RealtimeInterface.__init__(self, parent)

        self.saveButton.Bind( wx.EVT_BUTTON, self.saveSessionBpm )
        self.patientChoice.Bind( wx.EVT_CHOICE, self.selectPatient )
        # self.sessionChoice.Bind( wx.EVT_CHOICE, self.selectSession )

    def CloseTread(self, parent):
        self.worker = None
        processing.arduino.close()

    def bpmResult(self, event):
        self.bpmValue.SetLabel(event.data[0])
        self.ibiValue.SetLabel(event.data[1])

    def bpmStart(self, event):
        if not self.worker:
            print "SESSIONPATH: ", self.sessionPath
            processing.setSessionDir(self.sessionPath)
            self.worker = processing.BPMThread(self)
            self.bpmButton.SetLabel("Stop")
        else:
            self.worker.abort()
            self.worker = None
            self.bpmButton.Enable(False)
            self.bpmButton.SetLabel("Processing...")
            while processing.plotValidation == False:
                time.sleep(2)
                print "Still Processing..."

            print "Done processing"

            self.bpmButton.SetLabel("Done Processing")
            self.loadPatients()

    def calibrate(self, event):
        if not self.idTextCtrl.IsEmpty():
            self.idTextCtrl.Enable(False)
            self.sessionID = self.idTextCtrl.GetValue()
            self.sessionPath = sessionDir + self.sessionID + "/"

            if os.path.exists(self.sessionPath):
                wx.MessageBox('Please quit and select an unused ID', 'Existing ID', wx.OK | wx.ICON_INFORMATION)
            else:
                os.makedirs(self.sessionPath)

            if not self.worker:
                self.worker = processing.CalibrateThread(self)
                self.calibrateButton.SetLabel("Calibrating / Click to Stop")
            else:
                self.worker.abort()
                self.worker = None
                self.calibrateButton.SetLabel("Calibrate")
        else:
            wx.MessageBox('Please enter an ID for the session', 'No ID', wx.OK | wx.ICON_INFORMATION)

    def calibrateResult(self, event):
        if event.data == 1:
            self.worker = None
            print "calibrated"
            print "min: ", processing.getCalibrateLow()
            print "max: ", processing.getCalibrateHigh()
            print "mean: ", processing.getCalibrateMean()

            self.calibrateButton.Enable(False)
            self.calibrateButton.SetLabel("Calibrated")
            self.bpmButton.Enable(True)
        else:
            print "not calibrated"
            self.worker = None
        return

    def loadPatients(self):
        patientList = ["Select Patient"]
        for item in os.listdir(piPatientsDir):
            if not item.startswith('.'):
                patientList.append(item)

        self.patientChoice.AppendItems(patientList)

        self.patientChoice.SetSelection(0)
        self.patientChoice.Enable(True)

    def selectPatient(self, event):
        if self.patientChoice.GetSelection() != 0:
            self.saveButton.Enable(True)
        else:
            self.saveButton.Enable(False)

    def saveSessionBpm(self, event):
        selectedPatient = self.patientChoice.GetStringSelection()
        patientSessionsList = os.listdir(piPatientsDir + selectedPatient + "/")
        
        # get all the sessions
        allSessionsListFile = open(piPatientsDir + selectedPatient + "/allsessions.txt", 'r')
        sessionsList = allSessionsListFile.readlines()

        sessionPaths = []
        sessionTitles = []
        sessionSims = []
        sessionVals = []

        for session in sessionsList:
            sessionVals = session.split()
            
            sessionPaths.append(sessionVals[0])
            sessionTitles.append(sessionVals[1])
            sessionSims.append(sessionVals[2])


        self.latestSessionSavePath = piPatientsDir + selectedPatient + "/" + sessionPaths[-1]

        print "From: ", self.sessionPath
        print "To: ", self.latestSessionSavePath

        source = os.listdir(self.sessionPath)
        for files in source:
            shutil.copy(self.sessionPath + files, self.latestSessionSavePath)

        self.patientChoice.Enable(False)
        self.saveButton.Enable(False)
        self.saveButton.SetLabel("Saved")

        self.Close()

    def loadPatientSessions(self):
        pass




def main():
    app = wx.App()
    window = MainApp(None)
    window.Show(True)
    app.MainLoop()

if __name__ == '__main__':
    main()