import sys
sys.path.append("/Users/nahiyanmalik/Development/wxPython-src-3.0.0.0/wxPython")

import wx

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
        
        self.m_menuItem2 = wx.MenuItem( self.patientsMenu, wx.ID_ANY, u"New Patient", wx.EmptyString, wx.ITEM_NORMAL )
        self.patientsMenu.AppendItem( self.m_menuItem2 )
        
        self.newPatientMenuItem1 = wx.MenuItem( self.patientsMenu, wx.ID_ANY, u"Select Patient", wx.EmptyString, wx.ITEM_NORMAL )
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

    def firstPanel( self, event ):
        event.Skip()

    # def changeIntroPanel( self, event ):
    #     event.Skip()
    
    def __del__( self ):
        pass



class IntroPanel ( wx.Panel ):
    
    def __init__( self, parent ):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 600,400 ), style = wx.TAB_TRAVERSAL )
        
        introSizer = wx.BoxSizer( wx.VERTICAL )
        
        
        introSizer.AddSpacer( ( 0, 150), 0, 0, 5 )
        
        gSizer3 = wx.GridSizer( 1, 2, 0, 25 )
        
        self.selectPatientText = wx.StaticText( self, wx.ID_ANY, u"Select Patient", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.selectPatientText.Wrap( -1 )
        gSizer3.Add( self.selectPatientText, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        patientChoiceChoices = []
        self.patientChoice = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, patientChoiceChoices, 0 )
        self.patientChoice.SetSelection( 0 )
        gSizer3.Add( self.patientChoice, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        introSizer.Add( gSizer3, 0, wx.EXPAND, 5 )
        
        
        introSizer.AddSpacer( ( 0, 25), 0, 0, 5 )
        
        self.newCreatePatientBtn = wx.Button( self, wx.ID_ANY, u"Create Patient", wx.DefaultPosition, wx.DefaultSize, 0 )
        introSizer.Add( self.newCreatePatientBtn, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        self.SetSizer( introSizer )
        self.Layout()
    
    def __del__( self ):
        pass
    
    
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
        
        patientBtnSizer = wx.GridSizer( 2, 2, 0, 0 )
        
        self.createPatientBtn = wx.Button( self, wx.ID_ANY, u"Create Patient", wx.DefaultPosition, wx.DefaultSize, 0 )
        patientBtnSizer.Add( self.createPatientBtn, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
        
        self.cancelPatientBtn = wx.Button( self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
        patientBtnSizer.Add( self.cancelPatientBtn, 0, wx.ALL, 5 )
        
        patientSizer.Add( patientBtnSizer, 0, wx.EXPAND, 5 )
        
        self.SetSizer( patientSizer )
        self.Layout()
    
    def __del__( self ):
        pass


class PatientPanel ( wx.Panel ):
    
    def __init__( self, parent ):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 800,600 ), style = wx.TAB_TRAVERSAL )
        
        patientProfileSizer = wx.BoxSizer( wx.VERTICAL )
        
        self.patientNotebook = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.notebookProfilePanel = wx.Panel( self.patientNotebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer101 = wx.BoxSizer( wx.VERTICAL )
        
        patientFieldsSizer = wx.FlexGridSizer( 7, 2, 20, 0 )
        patientFieldsSizer.SetFlexibleDirection( wx.BOTH )
        patientFieldsSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        patientFieldsSizer.SetMinSize( wx.Size( -1,400 ) ) 
        
        patientFieldsSizer.AddSpacer( ( 0, 10), 1, wx.EXPAND, 5 )
        
        
        patientFieldsSizer.AddSpacer( ( 0, 10), 1, wx.EXPAND, 5 )
        
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
        
        self.m_button21 = wx.Button( self.notebookProfilePanel, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer101.Add( self.m_button21, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        self.notebookProfilePanel.SetSizer( bSizer101 )
        self.notebookProfilePanel.Layout()
        bSizer101.Fit( self.notebookProfilePanel )
        self.patientNotebook.AddPage( self.notebookProfilePanel, u"Patient Profile", False )
        self.sessionNotebookPanel = wx.Panel( self.patientNotebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer9 = wx.BoxSizer( wx.VERTICAL )
        
        self.sessionNotebookPanel.SetSizer( bSizer9 )
        self.sessionNotebookPanel.Layout()
        bSizer9.Fit( self.sessionNotebookPanel )
        self.patientNotebook.AddPage( self.sessionNotebookPanel, u"Run New Session", False )
        self.historyNotebookPanel = wx.Panel( self.patientNotebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer10 = wx.BoxSizer( wx.VERTICAL )
        
        self.historyNotebookPanel.SetSizer( bSizer10 )
        self.historyNotebookPanel.Layout()
        bSizer10.Fit( self.historyNotebookPanel )
        self.patientNotebook.AddPage( self.historyNotebookPanel, u"History of Sessions", False )
        
        patientProfileSizer.Add( self.patientNotebook, 1, wx.ALL|wx.EXPAND, 5 )
        
        bSizer91 = wx.BoxSizer( wx.VERTICAL )
        
        patientProfileSizer.Add( bSizer91, 1, wx.EXPAND, 5 )
        
        self.SetSizer( patientProfileSizer )
        self.Layout()
    
    def __del__( self ):
        pass
    