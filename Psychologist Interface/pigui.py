import sys
sys.path.append("/Users/nahiyanmalik/Development/wxPython-src-3.0.0.0/wxPython")

import wx

import sys
sys.path.append("/Users/nahiyanmalik/Development/wxPython-src-3.0.0.0/wxPython")

import wx

###########################################################################
## Class PsychologistInterfaceFrame
###########################################################################

class PsychologistInterfaceFrame ( wx.Frame ):
    
    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 600,400 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        mainFrameSizer = wx.BoxSizer( wx.VERTICAL )
        
        self.SetSizer( mainFrameSizer )
        self.Layout()
        self.mainMenuBar = wx.MenuBar( 0 )
        self.patientsMenu = wx.Menu()
        self.selectPatientMenuItem = wx.MenuItem( self.patientsMenu, wx.ID_ANY, u"Select Patient", wx.EmptyString, wx.ITEM_NORMAL )
        self.patientsMenu.AppendItem( self.selectPatientMenuItem )
        
        self.newPatientMenuItem1 = wx.MenuItem( self.patientsMenu, wx.ID_ANY, u"Create New Patient", wx.EmptyString, wx.ITEM_NORMAL )
        self.patientsMenu.AppendItem( self.newPatientMenuItem1 )
        
        self.mainMenuBar.Append( self.patientsMenu, u"Patients" ) 
        
        self.configMenu = wx.Menu()
        self.orMenuItem = wx.MenuItem( self.configMenu, wx.ID_ANY, u"Oculus Rift Settings", wx.EmptyString, wx.ITEM_NORMAL )
        self.configMenu.AppendItem( self.orMenuItem )
        
        self.bioMenuItem = wx.MenuItem( self.configMenu, wx.ID_ANY, u"Biometrics Settings", wx.EmptyString, wx.ITEM_NORMAL )
        self.configMenu.AppendItem( self.bioMenuItem )
        
        self.dirMenuItem = wx.MenuItem( self.configMenu, wx.ID_ANY, u"Directories", wx.EmptyString, wx.ITEM_NORMAL )
        self.configMenu.AppendItem( self.dirMenuItem )
        
        self.avMenuItem = wx.MenuItem( self.configMenu, wx.ID_ANY, u"Audio/Video", wx.EmptyString, wx.ITEM_NORMAL )
        self.configMenu.AppendItem( self.avMenuItem )
        
        self.mainMenuBar.Append( self.configMenu, u"Configurations" ) 
        
        self.helpMenu = wx.Menu()
        self.helpMenuItem = wx.MenuItem( self.helpMenu, wx.ID_ANY, u"Help", wx.EmptyString, wx.ITEM_NORMAL )
        self.helpMenu.AppendItem( self.helpMenuItem )
        
        self.contactMenuItem = wx.MenuItem( self.helpMenu, wx.ID_ANY, u"Contact", wx.EmptyString, wx.ITEM_NORMAL )
        self.helpMenu.AppendItem( self.contactMenuItem )
        
        self.aboutMenuItem = wx.MenuItem( self.helpMenu, wx.ID_ANY, u"About", wx.EmptyString, wx.ITEM_NORMAL )
        self.helpMenu.AppendItem( self.aboutMenuItem )
        
        self.mainMenuBar.Append( self.helpMenu, u"Help" ) 
        
        self.SetMenuBar( self.mainMenuBar )
        
        
        self.Centre( wx.BOTH )
    
    def __del__( self ):
        pass
    

###########################################################################
## Class IntroPanel
###########################################################################

class IntroPanel ( wx.Panel ):
    
    def __init__( self, parent ):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 600,400 ), style = wx.TAB_TRAVERSAL )
        
        introSizer = wx.BoxSizer( wx.VERTICAL )
        
        
        introSizer.AddSpacer( ( 0, 125), 0, 0, 5 )
        
        patientChoiceChoices = []
        self.patientChoice = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 250,-1 ), patientChoiceChoices, 0 )
        self.patientChoice.SetSelection( 0 )
        introSizer.Add( self.patientChoice, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        
        introSizer.AddSpacer( ( 0, 25), 0, 0, 5 )
        
        self.m_staticText26 = wx.StaticText( self, wx.ID_ANY, u"OR", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText26.Wrap( -1 )
        introSizer.Add( self.m_staticText26, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        
        introSizer.AddSpacer( ( 0, 25), 0, 0, 5 )
        
        self.newCreatePatientBtn = wx.Button( self, wx.ID_ANY, u"Create New Patient", wx.DefaultPosition, wx.Size( 150,-1 ), 0 )
        introSizer.Add( self.newCreatePatientBtn, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        self.SetSizer( introSizer )
        self.Layout()
    
    def __del__( self ):
        pass
    

###########################################################################
## Class PatientPanel
###########################################################################

class PatientPanel ( wx.Panel ):
    
    def __init__( self, parent ):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 800,600 ), style = wx.TAB_TRAVERSAL )
        
        patientProfileSizer = wx.BoxSizer( wx.VERTICAL )
        
        self.patientNotebook = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.notebookProfilePanel = wx.Panel( self.patientNotebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer101 = wx.BoxSizer( wx.VERTICAL )
        
        patientFieldsSizer = wx.FlexGridSizer( 6, 2, 10, 0 )
        patientFieldsSizer.SetFlexibleDirection( wx.BOTH )
        patientFieldsSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        self.fnameText = wx.StaticText( self.notebookProfilePanel, wx.ID_ANY, u"First Name*", wx.Point( -1,-1 ), wx.Size( 250,-1 ), wx.ALIGN_CENTRE )
        self.fnameText.Wrap( -1 )
        patientFieldsSizer.Add( self.fnameText, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.fnameTextCtrl = wx.TextCtrl( self.notebookProfilePanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 400,-1 ), 0 )
        patientFieldsSizer.Add( self.fnameTextCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.lnameText = wx.StaticText( self.notebookProfilePanel, wx.ID_ANY, u"Last Name*", wx.DefaultPosition, wx.Size( 250,-1 ), wx.ALIGN_CENTRE )
        self.lnameText.Wrap( -1 )
        patientFieldsSizer.Add( self.lnameText, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.lnameTextCtrl = wx.TextCtrl( self.notebookProfilePanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 400,-1 ), 0 )
        patientFieldsSizer.Add( self.lnameTextCtrl, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.dobText = wx.StaticText( self.notebookProfilePanel, wx.ID_ANY, u"Date of Birth*", wx.DefaultPosition, wx.Size( 250,-1 ), wx.ALIGN_CENTRE )
        self.dobText.Wrap( -1 )
        patientFieldsSizer.Add( self.dobText, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.dobDatePicker = wx.DatePickerCtrl( self.notebookProfilePanel, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.Size( 400,-1 ), wx.DP_DEFAULT )
        patientFieldsSizer.Add( self.dobDatePicker, 0, wx.ALL, 5 )
        
        self.genderText = wx.StaticText( self.notebookProfilePanel, wx.ID_ANY, u"Gender*", wx.DefaultPosition, wx.Size( 250,-1 ), wx.ALIGN_CENTRE )
        self.genderText.Wrap( -1 )
        patientFieldsSizer.Add( self.genderText, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        genderChoiceChoices = [ u"Male", u"Female" ]
        self.genderChoice = wx.Choice( self.notebookProfilePanel, wx.ID_ANY, wx.DefaultPosition, wx.Size( 400,-1 ), genderChoiceChoices, 0 )
        self.genderChoice.SetSelection( 0 )
        patientFieldsSizer.Add( self.genderChoice, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.patientIdText = wx.StaticText( self.notebookProfilePanel, wx.ID_ANY, u"Patient ID*", wx.DefaultPosition, wx.Size( 250,-1 ), wx.ALIGN_CENTRE )
        self.patientIdText.Wrap( -1 )
        patientFieldsSizer.Add( self.patientIdText, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.patientIdTextCtrl = wx.TextCtrl( self.notebookProfilePanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 400,-1 ), 0 )
        patientFieldsSizer.Add( self.patientIdTextCtrl, 0, wx.ALL, 5 )
        
        self.notesText = wx.StaticText( self.notebookProfilePanel, wx.ID_ANY, u"Notes", wx.DefaultPosition, wx.Size( 250,-1 ), wx.ALIGN_CENTRE )
        self.notesText.Wrap( -1 )
        patientFieldsSizer.Add( self.notesText, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        self.notesTextCtrl = wx.TextCtrl( self.notebookProfilePanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 400,100 ), wx.TE_MULTILINE )
        patientFieldsSizer.Add( self.notesTextCtrl, 1, wx.ALL|wx.EXPAND, 5 )
        
        bSizer101.Add( patientFieldsSizer, 0, wx.EXPAND, 5 )
        
        self.updatePatientBtn = wx.Button( self.notebookProfilePanel, wx.ID_ANY, u"Update Patient", wx.DefaultPosition, wx.Size( 150,-1 ), 0 )
        bSizer101.Add( self.updatePatientBtn, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        self.notebookProfilePanel.SetSizer( bSizer101 )
        self.notebookProfilePanel.Layout()
        bSizer101.Fit( self.notebookProfilePanel )
        self.patientNotebook.AddPage( self.notebookProfilePanel, u"Patient Profile", False )
        self.sessionNotebookPanel = wx.Panel( self.patientNotebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer9 = wx.BoxSizer( wx.VERTICAL )
        
        patientFieldsSizer1 = wx.FlexGridSizer( 7, 2, 10, 0 )
        patientFieldsSizer1.SetFlexibleDirection( wx.BOTH )
        patientFieldsSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        self.simTitleText = wx.StaticText( self.sessionNotebookPanel, wx.ID_ANY, u"Title", wx.Point( -1,-1 ), wx.Size( 250,-1 ), wx.ALIGN_CENTRE )
        self.simTitleText.Wrap( -1 )
        patientFieldsSizer1.Add( self.simTitleText, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.simTitleTextCtrl = wx.TextCtrl( self.sessionNotebookPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 400,-1 ), 0 )
        patientFieldsSizer1.Add( self.simTitleTextCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.simText = wx.StaticText( self.sessionNotebookPanel, wx.ID_ANY, u"Simulation", wx.DefaultPosition, wx.Size( 250,-1 ), wx.ALIGN_CENTRE )
        self.simText.Wrap( -1 )
        patientFieldsSizer1.Add( self.simText, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        simChioceChoices = []
        self.simChioce = wx.Choice( self.sessionNotebookPanel, wx.ID_ANY, wx.DefaultPosition, wx.Size( 400,-1 ), simChioceChoices, 0 )
        self.simChioce.SetSelection( 0 )
        patientFieldsSizer1.Add( self.simChioce, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.simNotesText = wx.StaticText( self.sessionNotebookPanel, wx.ID_ANY, u"Notes", wx.DefaultPosition, wx.Size( 250,-1 ), wx.ALIGN_CENTRE )
        self.simNotesText.Wrap( -1 )
        patientFieldsSizer1.Add( self.simNotesText, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        self.simNotesTextCtrl = wx.TextCtrl( self.sessionNotebookPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 400,100 ), wx.TE_MULTILINE )
        patientFieldsSizer1.Add( self.simNotesTextCtrl, 1, wx.ALL|wx.EXPAND, 5 )
        
        bSizer9.Add( patientFieldsSizer1, 0, wx.EXPAND, 5 )
        
        self.simStartBtn = wx.Button( self.sessionNotebookPanel, wx.ID_ANY, u"Start", wx.DefaultPosition, wx.Size( 150,-1 ), 0 )
        bSizer9.Add( self.simStartBtn, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        self.sessionNotebookPanel.SetSizer( bSizer9 )
        self.sessionNotebookPanel.Layout()
        bSizer9.Fit( self.sessionNotebookPanel )
        self.patientNotebook.AddPage( self.sessionNotebookPanel, u"Run New Session", False )
        self.historyNotebookPanel = wx.Panel( self.patientNotebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer10 = wx.BoxSizer( wx.VERTICAL )
        
        self.historyListPanel = wx.Panel( self.historyNotebookPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer10.Add( self.historyListPanel, 1, wx.EXPAND |wx.ALL, 5 )
        
        self.historyInfoPanel = wx.Panel( self.historyNotebookPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.historyInfoPanel.Hide()
        
        bSizer10.Add( self.historyInfoPanel, 1, wx.EXPAND |wx.ALL, 5 )
        
        self.historyNotebookPanel.SetSizer( bSizer10 )
        self.historyNotebookPanel.Layout()
        bSizer10.Fit( self.historyNotebookPanel )
        self.patientNotebook.AddPage( self.historyNotebookPanel, u"History of Sessions", False )
        
        patientProfileSizer.Add( self.patientNotebook, 1, wx.ALL|wx.EXPAND, 5 )
        
        self.SetSizer( patientProfileSizer )
        self.Layout()
    
    def __del__( self ):
        pass
    

###########################################################################
## Class CreatePatientPanel
###########################################################################

class CreatePatientPanel ( wx.Panel ):
    
    def __init__( self, parent ):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 600,400 ), style = wx.TAB_TRAVERSAL )
        
        patientSizer = wx.BoxSizer( wx.VERTICAL )
        
        patientFieldsSizer = wx.FlexGridSizer( 7, 2, 10, 20 )
        patientFieldsSizer.SetFlexibleDirection( wx.BOTH )
        patientFieldsSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        
        patientFieldsSizer.AddSpacer( ( 0, 3), 1, wx.EXPAND, 5 )
        
        
        patientFieldsSizer.AddSpacer( ( 0, 3), 1, wx.EXPAND, 5 )
        
        self.fnameText = wx.StaticText( self, wx.ID_ANY, u"First Name*", wx.Point( -1,-1 ), wx.Size( 125,-1 ), wx.ALIGN_CENTRE )
        self.fnameText.Wrap( -1 )
        patientFieldsSizer.Add( self.fnameText, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.fnameTextCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 400,-1 ), 0 )
        patientFieldsSizer.Add( self.fnameTextCtrl, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.lnameText = wx.StaticText( self, wx.ID_ANY, u"Last Name*", wx.DefaultPosition, wx.Size( 125,-1 ), wx.ALIGN_CENTRE )
        self.lnameText.Wrap( -1 )
        patientFieldsSizer.Add( self.lnameText, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.lnameTextCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 400,-1 ), 0 )
        patientFieldsSizer.Add( self.lnameTextCtrl, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.dobText = wx.StaticText( self, wx.ID_ANY, u"Date of Birth*", wx.DefaultPosition, wx.Size( 125,-1 ), wx.ALIGN_CENTRE )
        self.dobText.Wrap( -1 )
        patientFieldsSizer.Add( self.dobText, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.dobDatePicker = wx.DatePickerCtrl( self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.Size( 400,-1 ), wx.DP_DEFAULT )
        patientFieldsSizer.Add( self.dobDatePicker, 0, wx.ALL, 5 )
        
        self.genderText = wx.StaticText( self, wx.ID_ANY, u"Gender*", wx.DefaultPosition, wx.Size( 125,-1 ), wx.ALIGN_CENTRE )
        self.genderText.Wrap( -1 )
        patientFieldsSizer.Add( self.genderText, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        genderChoiceChoices = [ u"Male", u"Female" ]
        self.genderChoice = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 400,-1 ), genderChoiceChoices, 0 )
        self.genderChoice.SetSelection( 0 )
        patientFieldsSizer.Add( self.genderChoice, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.patientIdText = wx.StaticText( self, wx.ID_ANY, u"Patient ID*", wx.DefaultPosition, wx.Size( 125,-1 ), wx.ALIGN_CENTRE )
        self.patientIdText.Wrap( -1 )
        patientFieldsSizer.Add( self.patientIdText, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.patientIdTextCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 400,-1 ), 0 )
        patientFieldsSizer.Add( self.patientIdTextCtrl, 0, wx.ALL, 5 )
        
        self.notesText = wx.StaticText( self, wx.ID_ANY, u"Notes", wx.DefaultPosition, wx.Size( 125,-1 ), wx.ALIGN_CENTRE )
        self.notesText.Wrap( -1 )
        patientFieldsSizer.Add( self.notesText, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        self.notesTextCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 400,100 ), wx.TE_MULTILINE )
        patientFieldsSizer.Add( self.notesTextCtrl, 0, wx.ALL, 5 )
        
        patientSizer.Add( patientFieldsSizer, 0, wx.EXPAND, 5 )
        
        patientBtnSizer = wx.GridSizer( 2, 2, 0, 25 )
        
        self.createPatientBtn = wx.Button( self, wx.ID_ANY, u"Create Patient", wx.DefaultPosition, wx.Size( 150,-1 ), 0 )
        patientBtnSizer.Add( self.createPatientBtn, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
        
        self.cancelPatientBtn = wx.Button( self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.Size( 150,-1 ), 0 )
        patientBtnSizer.Add( self.cancelPatientBtn, 0, wx.ALL, 5 )
        
        patientSizer.Add( patientBtnSizer, 0, wx.EXPAND, 5 )
        
        self.SetSizer( patientSizer )
        self.Layout()
    
    def __del__( self ):
        pass
    

###########################################################################
## Class HistoryPanel
###########################################################################

class HistoryPanel ( wx.Panel ):
    
    def __init__( self, parent ):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 800,550 ), style = wx.TAB_TRAVERSAL )
        
        bSizer101 = wx.BoxSizer( wx.VERTICAL )
        
        patientFieldsSizer = wx.FlexGridSizer( 6, 2, 10, 0 )
        patientFieldsSizer.SetFlexibleDirection( wx.BOTH )
        patientFieldsSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        self.simTypeText = wx.StaticText( self, wx.ID_ANY, u"Simulation Type", wx.Point( -1,-1 ), wx.Size( 250,-1 ), wx.ALIGN_CENTRE )
        self.simTypeText.Wrap( -1 )
        patientFieldsSizer.Add( self.simTypeText, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        simChoiceChoices = []
        self.simChoice = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 400,-1 ), simChoiceChoices, 0 )
        self.simChoice.SetSelection( 0 )
        patientFieldsSizer.Add( self.simChoice, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        
        patientFieldsSizer.AddSpacer( ( 0, 10), 0, wx.EXPAND, 5 )
        
        bSizer101.Add( patientFieldsSizer, 0, wx.EXPAND, 5 )
        
        simHistoryCheckListChoices = []
        
        self.simHistoryCheckList = wx.CheckListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, simHistoryCheckListChoices, 0 ) 
        bSizer101.Add( self.simHistoryCheckList, 1, wx.ALL|wx.EXPAND, 5 )
        
        
        bSizer101.AddSpacer( ( 0, 10), 0, wx.EXPAND, 5 )
        
        self.plotComparisonsBtn = wx.Button( self, wx.ID_ANY, u"Plot Comparisons", wx.DefaultPosition, wx.Size( 150,-1 ), 0 )
        self.plotComparisonsBtn.Enable( False )
        
        bSizer101.Add( self.plotComparisonsBtn, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        
        bSizer101.AddSpacer( ( 0, 20), 0, wx.EXPAND, 5 )
        
        self.SetSizer( bSizer101 )
        self.Layout()
    
    def __del__( self ):
        pass
    

###########################################################################
## Class HistoryInformationPanel
###########################################################################

class HistoryInformationPanel ( wx.Panel ):
    
    def __init__( self, parent ):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 800,550 ), style = wx.TAB_TRAVERSAL )
        
        bSizer9 = wx.BoxSizer( wx.VERTICAL )
        
        patientFieldsSizer1 = wx.FlexGridSizer( 7, 2, 10, 0 )
        patientFieldsSizer1.SetFlexibleDirection( wx.BOTH )
        patientFieldsSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        self.histInfoTitleText = wx.StaticText( self, wx.ID_ANY, u"Title", wx.Point( -1,-1 ), wx.Size( 250,-1 ), wx.ALIGN_CENTRE )
        self.histInfoTitleText.Wrap( -1 )
        patientFieldsSizer1.Add( self.histInfoTitleText, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.histInfoTitleTextCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 400,-1 ), 0 )
        patientFieldsSizer1.Add( self.histInfoTitleTextCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.histInfoSimText = wx.StaticText( self, wx.ID_ANY, u"Simulation", wx.DefaultPosition, wx.Size( 250,-1 ), wx.ALIGN_CENTRE )
        self.histInfoSimText.Wrap( -1 )
        patientFieldsSizer1.Add( self.histInfoSimText, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.histInfoSimTextCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 400,-1 ), 0 )
        patientFieldsSizer1.Add( self.histInfoSimTextCtrl, 0, wx.ALL, 5 )
        
        self.histInfoNotesTexts = wx.StaticText( self, wx.ID_ANY, u"Notes", wx.DefaultPosition, wx.Size( 250,-1 ), wx.ALIGN_CENTRE )
        self.histInfoNotesTexts.Wrap( -1 )
        patientFieldsSizer1.Add( self.histInfoNotesTexts, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        self.histInfoNotesTextCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 400,100 ), wx.TE_MULTILINE )
        patientFieldsSizer1.Add( self.histInfoNotesTextCtrl, 1, wx.ALL|wx.EXPAND, 5 )
        
        bSizer9.Add( patientFieldsSizer1, 0, wx.EXPAND, 5 )
        
        self.sessionPlotBitmap = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer9.Add( self.sessionPlotBitmap, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        gSizer3 = wx.GridSizer( 1, 2, 0, 25 )
        
        self.updateSessionBtn = wx.Button( self, wx.ID_ANY, u"Update", wx.DefaultPosition, wx.Size( 150,-1 ), 0 )
        gSizer3.Add( self.updateSessionBtn, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.cancelInfoBtn = wx.Button( self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.Size( 150,-1 ), 0 )
        gSizer3.Add( self.cancelInfoBtn, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        bSizer9.Add( gSizer3, 0, wx.EXPAND, 5 )
        
        self.SetSizer( bSizer9 )
        self.Layout()
    
    def __del__( self ):
        pass