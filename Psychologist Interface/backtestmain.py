import sys
sys.path.append("/Users/nahiyanmalik/Development/wxPython-src-3.0.0.0/wxPython")

import wx
import pigui

import serial
import time
import datetime
import re

from threading import *
 
class MainApp(pigui.PsychologistInterfaceFrame):
    # def OnInit(self):
    #     frame = gui.RealtimeInterface(None)
    #     frame.Show(True)
    #     self.SetTopWindow(frame)
    #     self.frame = frame
    #     return True


    def OnInit(self, parent):
        pigui.PsychologistInterfaceFrame.__init__(self, parent)
        # pigui.PsychologistInterfaceFrame.__init__(self, parent, panel1, panel2)
        pigui.PsychologistInterfaceFrame.panelOne = Panel1(self)
        # self.panelTwo = Panel2(self)

        # self.panelTwo.Hide()

        pigui.PsychologistInterfaceFrame.firstPanel(self)

    def firstPanel(self, parent):
        

    

class Panel1(pigui.introPanel):

    def OnInit(self, parent):
        pigui.introPanel.__init__(self, parent)

    def changeIntroPanel( self, event ):
        if self.panelOne.IsShown():
            self.SetTitle("Panel Two Showing")
            self.PanelOne.Hide()
            self.PanelTwo.Show()
        else:
            self.SetTitle("Panel One Showing")
            self.PanelOne.Show()
            self.PanelTwo.Hide()
        self.Layout()

class Panel2(pigui.patientPanel):

    def OnInit(self, parent):
        pigui.patientPanel.__init__(self, parent)

    def changeIntroPanel( self, event ):
        if self.panelOne.IsShown():
            self.SetTitle("Panel Two Showing")
            self.PanelOne.Hide()
            self.PanelTwo.Show()
        else:
            self.SetTitle("Panel One Showing")
            self.PanelOne.Show()
            self.PanelTwo.Hide()
        self.Layout()






def main():
    app = wx.App()
    
    window = MainApp(None)
    p1 = Panel1(window)
    p2 = Panel2(window)
    p2.Hide()
    window.Show(True)
    app.MainLoop()

if __name__ == '__main__':
    main()