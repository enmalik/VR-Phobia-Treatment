import sys
sys.path.append("/Users/nahiyanmalik/Development/wxPython-src-3.0.0.0/wxPython")

import wx
import pigui

import serial
import time
import datetime
import re

from threading import *

appDirectory = "/Users/nahiyanmalik/Development/VR-Phobia-Treatment/Psychologist Interface/App/"
patientDirectory = appDirectory + "Patients/"
 
class MainApp(pigui.PsychologistInterfaceFrame):
    # def OnInit(self):
    #     frame = gui.RealtimeInterface(None)
    #     frame.Show(True)
    #     self.SetTopWindow(frame)
    #     self.frame = frame
    #     return True



    def __init__(self, parent):
        pigui.PsychologistInterfaceFrame.__init__(self, parent)
     
        self.introPanel = PanelIntro(self)
        self.createPanel = PanelCreate(self)
        self.patientPanel = PanelPatient(self)
        self.patientPanel.historyListPanel = PanelHistory(self.patientPanel.historyNotebookPanel)
        self.patientPanel.historyInfoPanel = PanelHistoryInfo(self.patientPanel.historyNotebookPanel)

        self.updatePanel("intro")
        self.updateHistoryPanel("list");

        self.introPanel.newCreatePatientBtn.Bind( wx.EVT_BUTTON, self.changeIntroPanel )
        self.createPanel.cancelPatientBtn.Bind( wx.EVT_BUTTON, self.cancelCreate )
        self.createPanel.createPatientBtn.Bind( wx.EVT_BUTTON, self.createPatient )

    # def firstPanel(self, parent):

    def changeIntroPanel( self, event ):
        self.updatePanel("create")

    def createPatient(self, event):
        self.updatePanel("patient")

    def cancelCreate(self, event):
        self.updatePanel("intro")
        # CREATE METHOD TO CLEAR ALL FIELDS

    def updatePanel(self, panel):
        if panel == "intro":
            width, height = 600, 400
            self.introPanel.Show()
            self.createPanel.Hide()
            self.patientPanel.Hide()
            self.setStaticSize(width, height)
        elif panel == "create":
            width, height = 600, 400
            self.introPanel.Hide()
            self.createPanel.Show()
            self.patientPanel.Hide()
            self.setStaticSize(width, height)
        elif panel == "patient":
            width, height = 800, 600
            self.introPanel.Hide()
            self.createPanel.Hide()
            self.patientPanel.Show()
            self.setStaticSize(width, height)
        self.Layout()

    def updateHistoryPanel(self, panel):
        if panel == "list":
            self.patientPanel.historyListPanel.Show()
            self.patientPanel.historyInfoPanel.Hide()
        elif panel == "info":
            self.patientPanel.historyListPanel.Hide()
            self.patientPanel.historyInfoPanel.Show()
        self.Layout()




    def setStaticSize(self, width, height):
        self.SetSizeWH(width, height)
        self.SetMaxSize((width, height))


    

class PanelIntro(pigui.IntroPanel):

    def __init__(self, parent):
        pigui.IntroPanel.__init__(self, parent)

    # def OnInit(self, parent):
    #     pigui.introPanel.__init__(self, parent)

    # def changeIntroPanel( self, event ):
    #     print "hi"
    #     if pigui.PsychologistInterfaceFrame.panelOne.IsShown():
    #         print "hi"
    #         # self.SetTitle("Panel Two Showing")
    #         # self.PanelOne.Hide()
    #         # self.PanelTwo.Show()
    #     else:
    #         print "no"
    #         # self.SetTitle("Panel One Showing")
    #         # self.PanelOne.Show()
    #         # self.PanelTwo.Hide()
    #     self.Layout()

class PanelPatient(pigui.PatientPanel):

    def __init__(self, parent):
        pigui.PatientPanel.__init__(self, parent)

    # def OnInit(self, parent):
    #     pigui.patientPanel.__init__(self, parent)

    def justDoingSomething():
        print "just doing something"

    # def changeIntroPanel( self, event ):
    #     if self.panelOne.IsShown():
    #         self.SetTitle("Panel Two Showing")
    #         self.PanelOne.Hide()
    #         self.PanelTwo.Show()
    #     else:
    #         self.SetTitle("Panel One Showing")
    #         self.PanelOne.Show()
    #         self.PanelTwo.Hide()
    #     self.Layout()

class PanelCreate(pigui.CreatePatientPanel):

    def __init__(self, parent):
        pigui.CreatePatientPanel.__init__(self, parent)


class PanelHistory(pigui.HistoryPanel):

    def __init__(self, parent):
        pigui.HistoryPanel.__init__(self, parent)

class PanelHistoryInfo(pigui.HistoryInformationPanel):

    def __init__(self, parent):
        pigui.HistoryInformationPanel.__init__(self, parent)







def main():
    app = wx.App()
    
    window = MainApp(None)
    # p1 = Panel1(window)
    # p2 = Panel2(window)
    # p2.Hide()
    window.Show(True)
    app.MainLoop()

if __name__ == '__main__':
    main()