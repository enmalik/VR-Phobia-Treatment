import sys
sys.path.append("/Users/nahiyanmalik/Development/wxPython-src-3.0.0.0/wxPython")

import serial
import time
import datetime
import re

from threading import *

import wx
import time
 
class MyForm(wx.Frame):
 
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Timer Tutorial 1", size=(500,500))
 
        # Add a panel so it looks the correct on all platforms
        panel = wx.Panel(self, wx.ID_ANY)
 
        self.toggleBtn = wx.Button(panel, wx.ID_ANY, "Start")
        self.toggleBtn.Bind(wx.EVT_BUTTON, self.onToggle)

        self.m_staticText1 = wx.StaticText( panel, wx.ID_ANY, "MyLabel")

        EVT_RESULT(self,self.OnResult)

        self.worker = None
 
    def onToggle(self, event):
        self.m_staticText1.SetLabel("test")
        if not self.worker:
            self.worker = WorkerThread(self)

    def OnResult(self, event):
        self.m_staticText1.SetLabel(event.data)

EVT_RESULT_ID = wx.NewId()

def EVT_RESULT(win, func):
    win.Connect(-1, -1, EVT_RESULT_ID, func)

class ResultEvent(wx.PyEvent):
    def __init__(self, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_RESULT_ID)
        self.data = data


class WorkerThread(Thread):
    def __init__(self, notify_window):
        Thread.__init__(self)
        self._notify_window = notify_window
        self._want_abort = 0
        self.start()

    def run(self):
        # arduino = serial.Serial('/dev/tty.usbmodem1421',115200)
        # receiving(arduino)
        for i in range(10):
            time.sleep(1)
            wx.PostEvent(self._notify_window, ResultEvent(str(i)))


    def abort(self):
        self._want_abort = 1

def receiving(ser):
    # regex = re.compile("[.*]_")
    while True:
        time.sleep(2)
        read = ser.read(ser.inWaiting())
        print read


 
# Run the program
if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = MyForm().Show()
    app.MainLoop()