import sys
sys.path.append("/Users/nahiyanmalik/Development/wxPython-src-3.0.0.0/wxPython")

import wx

wx.ID_mainPanel = 1000
wx.ID_calibrateButton = 1001
wx.ID_patientText = 1002
wx.ID_patientChoice = 1003
wx.ID_bpmButton = 1004
wx.ID_bpmLabel = 1005
wx.ID_bpmValue = 1006
wx.ID_ibiLabel = 1007
wx.ID_ibiValue = 1008

EVT_RESULT_ID = wx.NewId()

def EVT_RESULT(win, func):
    win.Connect(-1, -1, EVT_RESULT_ID, func)

EVT_CALIBRATE_ID = wx.NewId()

def EVT_CALIBRATE(win, func):
    win.Connect(-1, -1, EVT_CALIBRATE_ID, func)

class RealtimeInterface ( wx.Frame ):
    
    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Biometrics Monitor", pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        mainSizer = wx.BoxSizer( wx.VERTICAL )
        
        self.mainPanel = wx.Panel( self, wx.ID_mainPanel, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        mainPanelSizer = wx.BoxSizer( wx.VERTICAL )
        
        buttonSizer = wx.GridSizer( 1, 1, 0, 0 )
        
        self.calibrateButton = wx.Button( self.mainPanel, wx.ID_calibrateButton, u"Calibrate", wx.DefaultPosition, wx.DefaultSize, 0 )
        buttonSizer.Add( self.calibrateButton, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        mainPanelSizer.Add( buttonSizer, 0, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        gSizer2 = wx.GridSizer( 1, 3, 0, 0 )
        
        gSizer2.SetMinSize( wx.Size( -1,50 ) ) 
        self.patientText = wx.StaticText( self.mainPanel, wx.ID_patientText, u"Patient:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.patientText.Wrap( -1 )
        gSizer2.Add( self.patientText, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        patientChoiceChoices = []
        self.patientChoice = wx.Choice( self.mainPanel, wx.ID_patientChoice, wx.DefaultPosition, wx.DefaultSize, patientChoiceChoices, 0 )
        self.patientChoice.SetSelection( 0 )
        self.patientChoice.Enable( False )
        
        gSizer2.Add( self.patientChoice, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.bpmButton = wx.Button( self.mainPanel, wx.ID_bpmButton, u"Start", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.bpmButton.Enable( False )
        
        gSizer2.Add( self.bpmButton, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        mainPanelSizer.Add( gSizer2, 0, 0, 5 )
        
        gSizer3 = wx.GridSizer( 2, 2, 0, 0 )
        
        self.bpmLabel = wx.StaticText( self.mainPanel, wx.ID_bpmLabel, u"BPM:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.bpmLabel.Wrap( -1 )
        self.bpmLabel.SetFont( wx.Font( 24, 70, 90, 90, False, "Arial" ) )
        
        gSizer3.Add( self.bpmLabel, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        self.bpmValue = wx.StaticText( self.mainPanel, wx.ID_bpmValue, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.bpmValue.Wrap( -1 )
        self.bpmValue.SetFont( wx.Font( 24, 70, 90, 90, False, "Arial" ) )
        
        gSizer3.Add( self.bpmValue, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        self.ibiLabel = wx.StaticText( self.mainPanel, wx.ID_ibiLabel, u"IBI:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.ibiLabel.Wrap( -1 )
        self.ibiLabel.SetFont( wx.Font( 24, 70, 90, 90, False, "Arial" ) )
        
        gSizer3.Add( self.ibiLabel, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
        
        self.ibiValue = wx.StaticText( self.mainPanel, wx.ID_ibiValue, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.ibiValue.Wrap( -1 )
        self.ibiValue.SetFont( wx.Font( 24, 70, 90, 90, False, "Arial" ) )
        
        gSizer3.Add( self.ibiValue, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        mainPanelSizer.Add( gSizer3, 1, wx.EXPAND, 5 )
        
        self.mainPanel.SetSizer( mainPanelSizer )
        self.mainPanel.Layout()
        mainPanelSizer.Fit( self.mainPanel )
        mainSizer.Add( self.mainPanel, 1, wx.EXPAND |wx.ALL, 5 )
        
        self.SetSizer( mainSizer )
        self.Layout()
        
        self.Centre( wx.BOTH )
        
        # Connect Events
        self.Bind( wx.EVT_CLOSE, self.CloseThread )
        self.calibrateButton.Bind( wx.EVT_BUTTON, self.calibrate )
        self.patientChoice.Bind( wx.EVT_CHOICE, self.choosePatient )
        self.bpmButton.Bind( wx.EVT_BUTTON, self.bpmStart )

        EVT_RESULT(self,self.bpmResult)
        EVT_CALIBRATE(self,self.calibrateResult)

        self.worker = None
    
    def __del__( self ):
        pass
    
    
    # Virtual event handlers, overide them in your derived class
    def CloseThread( self, event ):
        event.Skip()

    def calibrate( self, event ):
        event.Skip()

    def calibrateResult( self, event ):
        event.Skip()
    
    def choosePatient( self, event ):
        event.Skip()
    
    def bpmStart( self, event ):
        event.Skip()

    def bpmResult( self, event ):
        event.Skip()
