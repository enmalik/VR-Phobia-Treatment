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


    def __init__(self, parent):
        pigui.PsychologistInterfaceFrame.__init__(self, parent)
        self.SetSizeWH(800, 600)
        self.panelOne = Panel1(self)
        # self.panelTwo = Panel2(self)
        # self.panelTwo.Hide()

        self.panelOne.m_button2.Bind( wx.EVT_BUTTON, self.changeIntroPanel )

    # def firstPanel(self, parent):

    def changeIntroPanel( self, event ):
        print "hi"
        self.panelOne.Hide()
        self.SetSizeWH(800, 600)
        self.panelTwo = Panel2(self)

        # if self.panelOne.IsShown():
        #     print "hi"
        #     self.SetTitle("Panel Two Showing")
        #     self.panelOne.Hide()
        #     self.panelTwo.Show()
        # else:
        #     print "no"
        #     self.SetTitle("Panel One Showing")
        #     self.panelOne.Show()
        #     self.panelTwo.Hide()
        # self.Layout()


    

class Panel1(pigui.introPanel):

    def __init__(self, parent):
        pigui.introPanel.__init__(self, parent)

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

class Panel2(pigui.patientPanel):

    def __init__(self, parent):
        pigui.patientPanel.__init__(self, parent)

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