import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import gaussian
from scipy.ndimage import filters
import shlex, subprocess
import json

sessionPath = "/Users/nahiyanmalik/Development/VR-Phobia-Treatment/Psychologist Interface/App/Patients/Test1 User/Sessions/Skyscraper/1-Skyscraper-Session1/"
videoPath = sessionPath + "video.mp4"

def on_pick(event):
    artist = event.artist
    xmouse, ymouse = event.mouseevent.xdata, event.mouseevent.ydata
    x, y = artist.get_xdata(), artist.get_ydata()
    ind = event.ind
    print 'x, y of mouse: {:.2f},{:.2f}'.format(xmouse, ymouse)
    print 'data point:', x[ind[0]], y[ind[0]]
    print time
    print np.where(time == x[ind[0]])
    timeIndex = np.where(time == x[ind[0]])
    print int(timeIndex[0])

    if unixTime[timeIndex] > startTime:
    	print "yes"
    	videoTime = int(unixTime[timeIndex] - startTime)

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

startTime = sessionData['startTime']


data = np.loadtxt(sessionPath + "data.txt", skiprows=0)

time = data[:,2]
bpm = data[:,3]
unixTime = data[:,1]

smoothBpm = gaussSmooth(bpm, len(time))

# plt.plot(time, bpm)

fig, ax = plt.subplots()

tolerance = 10 # points
ax.plot(time, smoothBpm, 'o-', picker=10)

fig.canvas.callbacks.connect('pick_event', on_pick)

plt.show()