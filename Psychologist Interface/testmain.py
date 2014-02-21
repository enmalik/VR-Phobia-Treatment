import sys
sys.path.append("/Users/nahiyanmalik/Development/wxPython-src-3.0.0.0/wxPython")

import wx
import pigui
import os
import json


resetDate = wx.DateTimeFromDMY(31, wx.DateTime.Dec, 2000)

appDirectory = "/Users/nahiyanmalik/Development/VR-Phobia-Treatment/Psychologist Interface/App/"
patientDirectory = appDirectory + "Patients/"
simDirectory = appDirectory + "Simulations/"

patientPath = []

patientList = []
 
class MainApp(pigui.PsychologistInterfaceFrame):
    # def OnInit(self):
    #     frame = gui.RealtimeInterface(None)
    #     frame.Show(True)
    #     self.SetTopWindow(frame)
    #     self.frame = frame
    #     return True

    global patientList

    def __init__(self, parent):
        pigui.PsychologistInterfaceFrame.__init__(self, parent)
     
        self.introPanel = PanelIntro(self)
        self.createPanel = PanelCreate(self)
        self.patientPanel = PanelPatient(self)
        self.patientPanel.historyListPanel = PanelHistory(self.patientPanel.historyNotebookPanel)
        self.patientPanel.historyInfoPanel = PanelHistoryInfo(self.patientPanel.historyNotebookPanel)

        self.setPanelTypes()
        self.loadUsers()

        # ONCE IS FINALIZED, SEND IN PANEL AND USE .type IN DEF
        self.updatePanel("intro")
        self.updateHistoryPanel("list");

        self.introPanel.newCreatePatientBtn.Bind( wx.EVT_BUTTON, self.changeIntroPanel )
        self.introPanel.patientChoice.Bind( wx.EVT_CHOICE, self.selectPatient )

        self.createPanel.cancelPatientBtn.Bind( wx.EVT_BUTTON, self.cancelCreate )
        self.createPanel.createPatientBtn.Bind( wx.EVT_BUTTON, self.createPatient )

    # def firstPanel(self, parent):

    def setPanelTypes(self):
        self.introPanel.type = "intro"
        self.createPanel.type = "create"
        self.patientPanel.type = "patient"
        self.patientPanel.historyListPanel.type = "list"
        self.patientPanel.historyInfoPanel.type = "info"

    def loadUsers(self):
        self.introPanel.patientChoice.Clear()
        global patientList
        patientList = ["Select Existing Patient"]

        for item in os.listdir(patientDirectory):
            if not item.startswith('.'):
                patientList.append(item)

        # patientList.extend(os.listdir(patientDirectory))

        self.introPanel.patientChoice.AppendItems(patientList)
        print "loaded users"
        print "patient list: ", patientList


    def selectPatient(self, event):
        selectedUser = self.introPanel.patientChoice.GetStringSelection()
        selectedIndex = self.introPanel.patientChoice.GetCurrentSelection()

        print selectedUser
        print self.introPanel.type
        
        if selectedIndex != 0:
            global patientPath
            patientPath = patientDirectory + selectedUser + "/"
            self.goToUser("patient", selectedUser)

        self.resetIntroPanel()

    def resetIntroPanel(self):
        self.introPanel.patientChoice.SetSelection(0)

    def resetCreatePanel(self):
        self.createPanel.fnameTextCtrl.Clear()
        self.createPanel.lnameTextCtrl.Clear()
        self.createPanel.dobDatePicker.SetValue(resetDate)
        self.createPanel.genderChoice.SetSelection(0)
        self.createPanel.patientIdTextCtrl.Clear()
        self.createPanel.notesTextCtrl.Clear()

    def goToUser(self, panel, user):
        self.updatePanel(panel)

        patientJson = patientPath + "info.json"

        if os.path.exists(patientJson):
            with open(patientJson, 'r') as f:
                userData = json.load(f)

            date = wx.DateTimeFromDMY(userData['dobDay'], userData['dobMonth'], userData['dobYear'])
            
            self.patientPanel.fnameTextCtrl.SetValue(userData['firstName'])
            self.patientPanel.lnameTextCtrl.SetValue(userData['lastName'])
            self.patientPanel.dobDatePicker.SetValue(date)
            self.patientPanel.genderChoice.SetSelection(userData['gender'])
            self.patientPanel.patientIdTextCtrl.SetValue(userData['patientID'])
            self.patientPanel.notesTextCtrl.SetValue(userData['notes'])

        else:
            wx.MessageBox('Could not load user', 'Problem', wx.OK | wx.ICON_INFORMATION)





    def changeIntroPanel( self, event ):
        self.updatePanel("create")

    # def createPatient(self, event):
    #     self.updatePanel("patient")

    def cancelCreate(self, event):
        self.updatePanel("intro")
        self.resetCreatePanel()

    def createPatient(self, event):
        if self.createPanel.fnameTextCtrl.GetValue() == "" or self.createPanel.lnameTextCtrl.GetValue() == "" or self.createPanel.patientIdTextCtrl.GetValue() == "":
            wx.MessageBox('Please fill out all the mandory (*) fields', 'Missing Information', wx.OK | wx.ICON_INFORMATION)
        else:
            newUser = self.createPanel.fnameTextCtrl.GetValue() + " " + self.createPanel.lnameTextCtrl.GetValue()
            global patientPath
            patientPath = patientDirectory + newUser + "/"
            if os.path.exists(patientPath):
                wx.MessageBox('Please enter a different name', 'Existing User', wx.OK | wx.ICON_INFORMATION)
            else:
                os.makedirs(patientPath)

                infoJsonPath = patientPath + "info.json"

                dob = self.createPanel.dobDatePicker.GetValue()
                dobDay, dobMonth, dobYear = dob.Day, dob.Month, dob.Year

                print dobDay, dobMonth, dobYear

                userData = {
                    "firstName":self.createPanel.fnameTextCtrl.GetValue(),
                    "lastName":self.createPanel.lnameTextCtrl.GetValue(),
                    "dobDay":dobDay,
                    "dobMonth":dobMonth,
                    "dobYear":dobYear,
                    "gender":self.createPanel.genderChoice.GetSelection(),
                    "patientID":self.createPanel.patientIdTextCtrl.GetValue(),
                    "notes":self.createPanel.notesTextCtrl.GetValue()
                }

                with open(infoJsonPath, 'w') as f:
                    json.dump(userData, f, indent=4)
                    f.write('\n')

                print userData

                self.loadUsers()
                self.goToUser("patient", newUser)
                self.resetCreatePanel()
        

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