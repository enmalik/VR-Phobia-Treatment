# import sys
# sys.path.append("/Users/nahiyanmalik/Development/wxPython-src-3.0.0.0/wxPython")

import wx
import pigui
import os
import json
import time
import shlex, subprocess
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import gaussian
from scipy.ndimage import filters
import win32com.client as comclt
import shutil

resetDate = wx.DateTimeFromDMY(31, wx.DateTime.Dec, 2000)


#######################################

# vlcMacDir = "/Applications/VLC.app/Contents/MacOS/VLC"
# vlcMacDir = '"C:/Program Files/VideoLAN/VLC/vlc.exe"'
vlcMacDir = '"C:/Program Files (x86)/VideoLAN/VLC/vlc.exe"'

# udkDir = '"C:/UDK/UDK-2013-03/Binaries/Win64/UDK.exe"'
udkDir = '"C:/UDK/Skyscrapper/Binaries/Win32/UDK.exe"'

frapsVidsDir = "F:/Videos/"

cwd = os.getcwd()

# appDirectory = "/Users/nahiyanmalik/Development/VR-Phobia-Treatment/Psychologist Interface/App/"
# appDirectory = "C:/Users/NM/Dropbox/FYDP/Windows/Psychologist Interface/App/"
# appDirectory = "C:/Users/Vithuran/Dropbox/FYDP/Windows/Psychologist Interface/App/"

appDirectory = cwd + "/App/"

patientDirectory = appDirectory + "Patients/"
simDirectory = appDirectory + "Simulations/"
sessionsDirectory = "Sessions/"
jsonFileName = "info.json"
sessionInfoJsonFileName = "sessionInfo.json"
allSessionsFileName = "allsessions.txt"
videoFileName = "video.avi"

####################

sessionStartTime = None
sessionPlotData = None

patientPath = ""
sessionVideoPath = ""

patientList = []
simList = []
 
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

        print self.introPanel.IsEnabled()

        self.setPanelTypes()
        self.loadUsers()

        # ONCE IS FINALIZED, SEND IN PANEL AND USE .type IN DEF
        self.updatePanel("intro")
        self.updateHistoryPanel("list");

        self.introPanel.newCreatePatientBtn.Bind( wx.EVT_BUTTON, self.changeIntroPanel )
        self.introPanel.patientChoice.Bind( wx.EVT_CHOICE, self.selectPatient )

        self.createPanel.cancelPatientBtn.Bind( wx.EVT_BUTTON, self.cancelCreate )
        self.createPanel.createPatientBtn.Bind( wx.EVT_BUTTON, self.createPatient )

        self.patientPanel.updatePatientBtn.Bind( wx.EVT_BUTTON, self.updatePatientInfo )
        self.patientPanel.simChoice.Bind( wx.EVT_CHOICE, self.simTitle )
        self.patientPanel.simStartBtn.Bind( wx.EVT_BUTTON, self.startSimulation )
        self.patientPanel.saveSessionBtn.Bind( wx.EVT_BUTTON, self.saveSimulation )
        self.patientPanel.cancelPatientBtn.Bind( wx.EVT_BUTTON, self.cancelPatient )

        # single click, regardless of checking or not, takes you to session. making it double click.
        # self.patientPanel.historyListPanel.simHistoryCheckList.Bind( wx.EVT_LISTBOX, self.historySessionSelect )

        self.patientPanel.historyListPanel.simHistoryCheckList.Bind( wx.EVT_LISTBOX_DCLICK, self.historySessionSelect )
        self.patientPanel.historyListPanel.simChoice.Bind( wx.EVT_CHOICE, self.historySimulationSelect )
        self.patientPanel.historyListPanel.plotComparisonsBtn.Bind( wx.EVT_BUTTON, self.plotTrendComparisons )

        self.patientPanel.historyInfoPanel.cancelInfoBtn.Bind( wx.EVT_BUTTON, self.cancelSessionInfo )
        self.patientPanel.historyInfoPanel.updateSessionBtn.Bind( wx.EVT_BUTTON, self.updateSessionInfo )
        self.patientPanel.historyInfoPanel.sessionPlotBitmap.Bind(wx.EVT_LEFT_DOWN, self.interactivePlot) 



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
        self.introPanel.patientChoice.SetSelection(0)
        print "loaded users"
        print "patient list: ", patientList

    def loadSims(self):
        self.patientPanel.simChoice.Clear()
        global simList
        simList = ["Select Simulation"]

        for item in os.listdir(simDirectory):
            if not item.startswith('.'):
                simList.append(item)

        # patientList.extend(os.listdir(patientDirectory))

        self.patientPanel.simChoice.AppendItems(simList)
        self.patientPanel.simChoice.SetSelection(0)
        print "loaded simulations"
        print "sim list: ", simList


    def selectPatient(self, event):
        selectedUser = self.introPanel.patientChoice.GetStringSelection()
        selectedIndex = self.introPanel.patientChoice.GetCurrentSelection()

        print selectedUser
        print self.introPanel.type
        
        if selectedIndex != 0:
            global patientPath
            patientPath = patientDirectory + selectedUser + "/"
            self.goToPatient("patient", selectedUser)

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

    def goToPatient(self, panel, user):
        self.updatePanel(panel)

        patientJson = patientPath + jsonFileName

        self.loadHistoryList("All")


        if os.path.exists(patientJson):
            jsonFile = open(patientJson, "r")
            userData = json.load(jsonFile)
            jsonFile.close()

            date = wx.DateTimeFromDMY(userData['dobDay'], userData['dobMonth'], userData['dobYear'])
            
            self.patientPanel.fnameTextCtrl.SetValue(userData['firstName'])
            self.patientPanel.lnameTextCtrl.SetValue(userData['lastName'])
            self.patientPanel.dobDatePicker.SetValue(date)
            self.patientPanel.genderChoice.SetSelection(userData['gender'])
            self.patientPanel.patientIdTextCtrl.SetValue(userData['patientID'])
            self.patientPanel.notesTextCtrl.SetValue(userData['notes'])

            self.loadSims()
            self.loadHistorySimChoices()
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
                # os.makedirs(patientPath)
                os.makedirs(patientPath + "Sessions/")

                infoJsonPath = patientPath + jsonFileName
                allSessionsPath = patientPath + allSessionsFileName

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

                # with open(infoJsonPath, 'w') as f:
                #     json.dump(userData, f, indent=4)
                #     f.write('\n')

                jsonFile = open(infoJsonPath, "w")
                jsonFile.write(json.dumps(userData, indent = 4))
                jsonFile.close()

                open(allSessionsPath, 'w')

                print userData

                self.loadUsers()
                self.goToPatient("patient", newUser)
                self.resetCreatePanel()

    def updatePatientInfo(self, event):
        if self.patientPanel.fnameTextCtrl.GetValue() == "" or self.patientPanel.lnameTextCtrl.GetValue() == "" or self.patientPanel.patientIdTextCtrl.GetValue() == "":
            wx.MessageBox('Please fill out all the mandory (*) fields', 'Missing Information', wx.OK | wx.ICON_INFORMATION)
        else:
            global patientPath

            patientJson = patientPath + jsonFileName
            jsonFile = open(patientJson, "r")
            userData = json.load(jsonFile)
            jsonFile.close()

            dob = self.patientPanel.dobDatePicker.GetValue()
            dobDay, dobMonth, dobYear = dob.Day, dob.Month, dob.Year

            userData['patientID'] = self.patientPanel.patientIdTextCtrl.GetValue()
            userData['gender'] = self.patientPanel.genderChoice.GetSelection()
            userData['notes'] = self.patientPanel.notesTextCtrl.GetValue()


            jsonFile = open(patientJson, "w+")
            jsonFile.write(json.dumps(userData, indent = 4))
            jsonFile.close()

        print self

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

    def cancelPatient(self, event):
        self.updatePanel("intro")
        self.resetStartSimulationPanel()
        self.resetHistoryInfoPanel()


    def simTitle(self, event):
        selectedSim = self.patientPanel.simChoice.GetStringSelection()
        selectedIndex = self.patientPanel.simChoice.GetCurrentSelection()
        
        if selectedIndex != 0:
            # with open(patientPath + allSessionsFileName, 'r') as f:
            #     sessionsList = [line.strip() for line in f]

            # get all the sessions
            allSessionsListFile = open(patientPath + allSessionsFileName, 'r')
            sessionsList = allSessionsListFile.readlines()

            print sessionsList
            print len(sessionsList)

            if not os.path.exists(patientPath + sessionsDirectory + selectedSim):
                self.sessionNum = 1
            else:
                # get the specific sessions of selected simulation
                selectedSimSessionList = []
                for item in os.listdir(patientPath + sessionsDirectory + selectedSim):
                    if not item.startswith('.'):
                        selectedSimSessionList.append(item)

                print "sessionlist: ", selectedSimSessionList
                self.sessionNum = len(selectedSimSessionList) + 1

            self.allSessionsNum = len(sessionsList) + 1
            self.newSessionTitle = str(self.allSessionsNum) + "-" + selectedSim + "-Session" + str(self.sessionNum)
            self.patientPanel.simTitleTextCtrl.SetValue(self.newSessionTitle)

            self.newSessionPath = sessionsDirectory + selectedSim + "/" + self.newSessionTitle + "/"
            print self.newSessionPath
        else:
            self.patientPanel.simTitleTextCtrl.Clear()

    def startSimulation(self, event):
        self.resetHistoryListPanel()

        selectedSim = self.patientPanel.simChoice.GetStringSelection()
        selectedIndex = self.patientPanel.simChoice.GetCurrentSelection()

        print self.patientPanel.simStartBtn.GetLabel()

        if selectedIndex != 0:
            if not os.path.exists(patientPath + self.newSessionPath):
                os.makedirs(patientPath + self.newSessionPath)

                unixTime = time.time()

                with open(patientPath + allSessionsFileName, "a") as myfile:
                    myfile.write(self.newSessionPath + "\t" + self.newSessionTitle + "\t" + selectedSim + "\n")

                self.sessionInfoJsonPath = patientPath + self.newSessionPath + sessionInfoJsonFileName
                allSessionsPath = patientPath + allSessionsFileName

                print self.sessionInfoJsonPath

                sessionData = {
                    "title":self.newSessionTitle,
                    "simulation":selectedSim,
                    "notes":self.patientPanel.simNotesTextCtrl.GetValue(),
                    "startTime":unixTime,
                }

                jsonFile = open(self.sessionInfoJsonPath, "w")
                jsonFile.write(json.dumps(sessionData, indent = 4))
                jsonFile.close()

                self.patientPanel.simChoice.Enable(False)
                self.patientPanel.simStartBtn.Enable(False)
                self.patientPanel.simStartBtn.SetLabel("Running...")
                self.patientPanel.saveSessionBtn.Enable(True)

                command_line = udkDir
                print command_line
                args = shlex.split(command_line)
                p = subprocess.Popen(args)

                time.sleep(5)

                wsh = comclt.Dispatch("Wscript.Shell")
                wsh.SendKeys("{F9}")

                # print os.path.normpath(vlcMacDir) + vlcMacOptions + patientPath + os.path.normpath(self.newSessionPath) + vlcMacFileName
                # print os.path.normpath(vlcMacDir) + vlcMacOptions + os.path.normpath(patientPath + self.newSessionPath) + "/" + vlcMacFileName
                # print ""
                # os.system(os.path.normpath(vlcMacDir) + vlcMacOptions + patientPath + os.path.normpath(self.newSessionPath) + "/" + vlcMacFileName)

            else:
                wx.MessageBox('Session already exists', 'Session Exists', wx.OK | wx.ICON_INFORMATION)

    def saveSimulation(self, event):
        print self.patientPanel.simStartBtn.IsEnabled()
        print patientPath

        self.patientPanel.saveSessionBtn.Enable(False)
        self.patientPanel.saveSessionBtn.SetLabel("Saving...")

        jsonFile = open(self.sessionInfoJsonPath, "r")
        sessionData = json.load(jsonFile)
        jsonFile.close()

        sessionData['notes'] = self.patientPanel.simNotesTextCtrl.GetValue()

        

        wsh = comclt.Dispatch("Wscript.Shell")
        wsh.SendKeys("{F9}")

        time.sleep(5)

        videoSrc = os.listdir(frapsVidsDir)
        videoFile = videoSrc[-1]
        # shutil.move(frapsVidsDir + videoFile, patientPath + self.newSessionPath + videoFileName) # no more moving
        sessionData['videoFile'] = videoFile

        jsonFile = open(self.sessionInfoJsonPath, "w+")
        jsonFile.write(json.dumps(sessionData, indent = 4))
        jsonFile.close()
        
        self.loadHistoryList("All")
        self.patientPanel.patientNotebook.SetSelection(2)

        self.resetStartSimulationPanel()

        # updatePanel

    def loadHistoryList(self, simType):
        self.patientPanel.historyListPanel.simHistoryCheckList.Clear()
        print "load history list: ", simType

        if simType != "All":
            print "enable button"
            self.patientPanel.historyListPanel.plotComparisonsBtn.Enable(True)
        elif simType == "All":
            print "disable button"
            self.patientPanel.historyListPanel.plotComparisonsBtn.Enable(False)

        # get all the sessions
        allSessionsListFile = open(patientPath + allSessionsFileName, 'r')
        sessionsList = allSessionsListFile.readlines()

        self.sessionPaths = []
        self.sessionTitles = []
        self.sessionSims = []
        sessionVals = []

        for session in sessionsList:
            sessionVals = session.split()
            if simType != "All" and sessionVals[2] == simType:
                print "in"
                self.sessionPaths.append(sessionVals[0])
                self.sessionTitles.append(sessionVals[1])
                self.sessionSims.append(sessionVals[2])
            elif simType == "All":
                print "in else"
                self.sessionPaths.append(sessionVals[0])
                self.sessionTitles.append(sessionVals[1])
                self.sessionSims.append(sessionVals[2])

        print "session titles: ", self.sessionTitles

        self.patientPanel.historyListPanel.simHistoryCheckList.AppendItems(self.sessionTitles)

    def plotTrendComparisons(self, event):
        print self.patientPanel.historyListPanel.simHistoryCheckList.GetChecked()
        trendList = self.patientPanel.historyListPanel.simHistoryCheckList.GetChecked()
        print type(trendList)
        print len(trendList)

        # print self.sessionPaths
        # print self.sessionTitles

        simType = self.patientPanel.historyListPanel.simChoice.GetStringSelection()
        self.sessionTrendList = []
        
        fig = plt.figure()
        fig.suptitle('Heart-Rates of Sessions Over Time', fontsize=14, fontweight='bold')
        plot = fig.add_subplot(111)
        plot.set_xlabel('Time (Seconds)')
        plot.set_ylabel('Heart-Rate (Beats Per Minute)')

        for sessionIndex in trendList:
            sessionPath = self.sessionPaths[sessionIndex]
            self.sessionTrendList.append(sessionPath)

            sessionData = np.loadtxt(patientPath + sessionPath + "data.txt", skiprows=0)
            time = sessionData[:,2]
            bpm = sessionData[:,3]
            smoothBpm = gaussSmooth(bpm, len(time))
            plt.plot(time, smoothBpm, label = self.sessionTitles[sessionIndex])


        print self.sessionTrendList

        if len(trendList) == 0:
            wx.MessageBox('Please choose sessions to be plotted', 'No Sessions Selected', wx.OK | wx.ICON_INFORMATION)
        else:
            # wx.MessageBox('Will show plots of\n' + str(self.sessionTrendList), 'To Be Implemented', wx.OK | wx.ICON_INFORMATION)
            plt.legend(loc='best')
            plt.show()


    def resetHistoryListPanel(self):
        self.patientPanel.historyListPanel.simChoice.SetSelection(0)
        self.patientPanel.historyListPanel.simHistoryCheckList.SetSelection(-1)
        self.patientPanel.historyListPanel.simHistoryCheckList.Clear()
        self.patientPanel.historyListPanel.plotComparisonsBtn.Enable(False)


    def loadHistorySimChoices(self):
        self.patientPanel.historyListPanel.simChoice.Clear()
        historySimList = ["All"]

        for item in os.listdir(simDirectory):
            if not item.startswith('.'):
                historySimList.append(item)
        self.patientPanel.historyListPanel.simChoice.AppendItems(historySimList)
        self.patientPanel.historyListPanel.simChoice.SetSelection(0)


    def historySessionSelect(self, event):
        self.selectedSessionIndex = self.patientPanel.historyListPanel.simHistoryCheckList.GetSelection()
        print self.sessionPaths[self.selectedSessionIndex]
        self.patientPanel.historyListPanel.simHistoryCheckList.SetSelection(-1)

        self.goToSessionInfo(self.sessionPaths[self.selectedSessionIndex])

    def goToSessionInfo(self, relativeSessionPath):
        self.updateHistoryPanel("info")
        
        self.sessionPath = patientPath + relativeSessionPath
        sessionJson = self.sessionPath + sessionInfoJsonFileName

        if os.path.exists(sessionJson):
            jsonFile = open(sessionJson, "r")
            sessionData = json.load(jsonFile)
            jsonFile.close()

            global sessionVideoPath
            sessionVideoPath = frapsVidsDir + sessionData['videoFile']
            
            formattedDate = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(sessionData['startTime']))

            self.patientPanel.historyInfoPanel.simTextCtrl.SetValue(sessionData['simulation'])
            self.patientPanel.historyInfoPanel.histInfoTitleTextCtrl.SetValue(sessionData['title'])
            self.patientPanel.historyInfoPanel.sessionDateTextCtrl.SetValue(formattedDate)
            self.patientPanel.historyInfoPanel.histInfoNotesTextCtrl.SetValue(sessionData['notes'])

            

            if os.path.exists(self.sessionPath + "smooth-plot-small.png"):
                imgFile = self.sessionPath + "smooth-plot-small.png"
                img = wx.Image(imgFile, wx.BITMAP_TYPE_PNG)
                self.patientPanel.historyInfoPanel.sessionPlotBitmap.SetBitmap(wx.BitmapFromImage(img))

        else:
            wx.MessageBox('Could not load Session', 'Problem', wx.OK | wx.ICON_INFORMATION)

    def interactivePlot(self, event):
        print "hello"

        sessionPath = self.sessionPath
        # global videoPath
        # videoPath = sessionPath + videoFileName

        jsonFile = open(sessionPath + "sessionInfo.json", "r")
        sessionData = json.load(jsonFile)
        jsonFile.close()

        global sessionStartTime, sessionPlotData
        sessionStartTime = sessionData['startTime']
        sessionPlotData = np.loadtxt(sessionPath + "data.txt", skiprows=0)



        smoothBpm = gaussSmooth(sessionPlotData[:,3], len(sessionPlotData[:,2]))

        fig, ax = plt.subplots()
        fig.suptitle('Session Heart-Rate Over Time (click points to open video)', fontsize=14, fontweight='bold')
        plot = fig.add_subplot(111)
        plot.set_xlabel('Time (Seconds)')
        plot.set_ylabel('Heart-Rate (Beats Per Minute)')

        tolerance = 10 # points
        ax.plot(sessionPlotData[:,2], smoothBpm, 'o-', picker=10)

        fig.canvas.callbacks.connect('pick_event', on_pick)

        plt.show()

    def updateSessionInfo(self, event):
        relativeSessionPath = self.sessionPaths[self.selectedSessionIndex]

        sessionPath = patientPath + relativeSessionPath
        sessionJson = sessionPath + sessionInfoJsonFileName

        jsonFile = open(sessionJson, "r")
        sessionData = json.load(jsonFile)
        jsonFile.close()
            
        sessionData['simulation'] = self.patientPanel.historyInfoPanel.simTextCtrl.GetValue()
        sessionData['title'] = self.patientPanel.historyInfoPanel.histInfoTitleTextCtrl.GetValue()
        sessionData['notes'] = self.patientPanel.historyInfoPanel.histInfoNotesTextCtrl.GetValue()

        jsonFile = open(sessionJson, "w+")
        jsonFile.write(json.dumps(sessionData, indent = 4))
        jsonFile.close()

        self.resetHistoryInfoPanel()

    def historySimulationSelect(self, event):
        simType = self.patientPanel.historyListPanel.simChoice.GetStringSelection()
        print simType
        self.loadHistoryList(simType)




    def cancelSessionInfo(self, event):
        self.resetHistoryInfoPanel()

    def resetHistoryInfoPanel(self):
        self.updateHistoryPanel("list")
        self.patientPanel.historyInfoPanel.simTextCtrl.Clear()
        self.patientPanel.historyInfoPanel.histInfoTitleTextCtrl.Clear()
        self.patientPanel.historyInfoPanel.sessionDateTextCtrl.Clear()
        self.patientPanel.historyInfoPanel.histInfoNotesTextCtrl.Clear()


    def resetStartSimulationPanel(self):
        self.patientPanel.simChoice.Enable(True)
        self.patientPanel.simChoice.SetSelection(0)
        self.patientPanel.simTitleTextCtrl.Clear()
        self.patientPanel.simNotesTextCtrl.Clear()
        self.patientPanel.simStartBtn.Enable(True)
        self.patientPanel.simStartBtn.SetLabel("Start")
        self.patientPanel.saveSessionBtn.Enable(False)
        self.patientPanel.saveSessionBtn.SetLabel("Save")
        self.sessionInfoJsonPath = None
        self.allSessionsNum = None
        self.newSessionTitle = None
        self.newSessionPath = None


    def setStaticSize(self, width, height):
        self.SetSizeWH(width, height)
        # self.SetMaxSize((width, height))


    

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

def gaussSmooth(vals, num):
    b = gaussian(num, 1)
    smoothVals = filters.convolve1d(vals, b/b.sum())
    return smoothVals

def on_pick(event):
    global sessionPlotData, sessionStartTime, sessionVideoPath
    artist = event.artist
    xmouse, ymouse = event.mouseevent.xdata, event.mouseevent.ydata
    x, y = artist.get_xdata(), artist.get_ydata()
    ind = event.ind
    print 'x, y of mouse: {:.2f},{:.2f}'.format(xmouse, ymouse)
    print 'data point:', x[ind[0]], y[ind[0]]
    print sessionPlotData[:,2]
    print np.where(sessionPlotData[:,2] == x[ind[0]])
    timeIndex = np.where(sessionPlotData[:,2] == x[ind[0]])
    print int(timeIndex[0])

    if sessionPlotData[:,1][timeIndex] > sessionStartTime:
        print "yes"
        videoTime = int(sessionPlotData[:,1][timeIndex] - sessionStartTime)

        # command_line = vlcMacDir.replace(" ", "\ ") + " " + videoPath.replace(" ", "\ ") + " --start-time " + str(videoTime)
        command_line = vlcMacDir + ' "' + sessionVideoPath.replace("/", "\\") + '" --start-time='  + str(videoTime)
        print command_line
        command_line = str(command_line)

        args = shlex.split(command_line)
        print args
        p = subprocess.Popen(args)

    else:
        print "no"

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
