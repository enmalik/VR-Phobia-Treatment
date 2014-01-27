import sys
sys.path.append("/Users/nahiyanmalik/Development/wxPython-src-3.0.0.0/wxPython")

import wx

wx.ID_mainPanel = 1000
wx.ID_startButton = 1001
wx.ID_stopButton = 1002
wx.ID_bpmLabel = 1003
wx.ID_ibiLabel = 1004

def EVT_RESULT(win, func):
    win.Connect(-1, -1, EVT_RESULT_ID, func)

EVT_RESULT_ID = wx.NewId()

class RealtimeInterface ( wx.Frame ):
    
    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        mainSizer = wx.BoxSizer( wx.VERTICAL )
        
        self.mainPanel = wx.Panel( self, wx.ID_mainPanel, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        mainPanelSizer = wx.BoxSizer( wx.VERTICAL )
        
        buttonSizer = wx.GridSizer( 2, 2, 0, 0 )
        
        self.startButton = wx.Button( self.mainPanel, wx.ID_startButton, u"Start", wx.DefaultPosition, wx.DefaultSize, 0 )
        buttonSizer.Add( self.startButton, 0, wx.ALL, 5 )
        
        self.stopButton = wx.Button( self.mainPanel, wx.ID_stopButton, u"Stop", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stopButton.Enable( False )
        
        buttonSizer.Add( self.stopButton, 0, wx.ALL, 5 )
        
        self.bpmLabel = wx.StaticText( self.mainPanel, wx.ID_bpmLabel, u"BPM", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.bpmLabel.Wrap( -1 )
        buttonSizer.Add( self.bpmLabel, 0, wx.ALL, 5 )
        
        self.ibiLabel = wx.StaticText( self.mainPanel, wx.ID_ibiLabel, u"IBI", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.ibiLabel.Wrap( -1 )
        buttonSizer.Add( self.ibiLabel, 0, wx.ALL, 5 )
        
        mainPanelSizer.Add( buttonSizer, 1, wx.EXPAND, 5 )
        
        self.mainPanel.SetSizer( mainPanelSizer )
        self.mainPanel.Layout()
        mainPanelSizer.Fit( self.mainPanel )
        mainSizer.Add( self.mainPanel, 1, wx.EXPAND |wx.ALL, 5 )
        
        self.SetSizer( mainSizer )
        self.Layout()
        
        self.Centre( wx.BOTH )
        
        # Connect Events
        self.startButton.Bind( wx.EVT_BUTTON, self.bpmStart )

        EVT_RESULT(self,self.bpmResult)

        self.worker = None

    def bpmStart( self, event ):
        event.Skip()

    def bpmResult( self, event ):
        event.Skip()

    # def bpmResult( self, event ):
    #     event.Skip()

    def __del__( self ):
        pass
        self.m_staticText1.SetLabel(event.data)

# if __name__ == "__main__":
#     app = wx.PySimpleApp()
#     frame = RealtimeInterface(None).Show()
#     app.MainLoop()