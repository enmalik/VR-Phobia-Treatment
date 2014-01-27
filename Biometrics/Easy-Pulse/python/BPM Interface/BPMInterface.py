import sys

sys.path.append("/Users/nahiyanmalik/Development/wxPython-src-3.0.0.0/wxPython")

import wx

app = wx.App()
frame = wx.Frame(None, -1, 'simple.py')
frame.Show()

app.MainLoop()
