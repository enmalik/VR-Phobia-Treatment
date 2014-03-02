import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import gaussian
from scipy.ndimage import filters
import shlex, subprocess
import json

sessionPath = "/Users/nahiyanmalik/Development/VR-Phobia-Treatment/Psychologist Interface/App/Patients/N M/Sessions/Skyscraper/1-Skyscraper-Session1/"
videoPath = sessionPath + "video.mp4"

def on_pick(event):
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

    	command_line = vlcMacDir.replace(" ", "\ ") + " " + videoPath.replace(" ", "\ ") + " --start-time " + str(videoTime)
        print command_line

        args = shlex.split(command_line)
        p = subprocess.Popen(args)

    else:
    	print "no"

def gaussSmooth(vals, num):
    b = gaussian(num, 1)
    smoothVals = filters.convolve1d(vals, b/b.sum())
    return smoothVals

# fig, ax = plt.subplots()

# tolerance = 10 # points
# ax.plot(range(10), 'ro-', picker=tolerance)

vlcMacDir = "/Applications/VLC.app/Contents/MacOS/VLC"

jsonFile = open(sessionPath + "sessionInfo.json", "r")
sessionData = json.load(jsonFile)
jsonFile.close()

global sessionStartTime, sessionPlotData
sessionStartTime = sessionData['startTime']
sessionPlotData = np.loadtxt(sessionPath + "data.txt", skiprows=0)



smoothBpm = gaussSmooth(sessionPlotData[:,3], len(sessionPlotData[:,2]))

# plt.plot(time, bpm)

fig, ax = plt.subplots()

tolerance = 10 # points
ax.plot(sessionPlotData[:,2], smoothBpm, 'o-', picker=10)

fig.canvas.callbacks.connect('pick_event', on_pick)

plt.show()