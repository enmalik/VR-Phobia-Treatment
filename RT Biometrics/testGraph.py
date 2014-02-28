import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.ndimage import filters

from scipy.signal import gaussian


import processing

def nan_helper(y):
    """Helper to handle indices and logical indices of NaNs.

    Input:
        - y, 1d numpy array with possible NaNs
    Output:
        - nans, logical indices of NaNs
        - index, a function, with signature indices= index(logical_indices),
          to convert logical indices of NaNs to 'equivalent' indices
    Example:
        >>> # linear interpolation of NaNs
        >>> nans, x= nan_helper(y)
        >>> y[nans]= np.interp(x(nans), x(~nans), y[~nans])
    """

    return np.isnan(y), lambda z: z.nonzero()[0]

def gaussSmooth(vals, num):
	b = gaussian(num, 1)
	smoothVals = filters.convolve1d(vals, b/b.sum())
	return smoothVals

data = np.loadtxt("writefile.txt", skiprows=0)

print data

time = data[:,2]
bpm = data[:,3]

nans, x = nan_helper(bpm)
bpm[nans]= np.interp(x(nans), x(~nans), bpm[~nans])


# fig = plt.gcf()
# fig.suptitle('Session Heart-Rate Over Time', fontsize=14, fontweight='bold')
# plot1 = fig.add_subplot(111)
# # plot1.set_title('axes title')
# plot1.set_xlabel('Time (Seconds)')
# plot1.set_ylabel('Heart-Rate (Beats Per Minute)')
# fig.set_size_inches(18.5,10.5)
# plt.plot(time, bpm)


# plt.savefig('saved-plot.png', dpi = 250)

# plt.show()
# time = data[:,2]
# bpm = data[:,3]

numTimes = len(time)

cubicSpline = interp1d(time, bpm, kind='cubic')
timeNew = np.linspace(time.min(), time.max(), 40)

print time
print timeNew

# print len(cubicSpline), len(timeNew)
print len(timeNew)

# plt.plot(timeNew, cubicSpline(timeNew))
# plt.show()


bpmGaussSmooth = gaussSmooth(bpm, numTimes)

print len(time), len(bpmGaussSmooth)

fig = plt.gcf()
fig.suptitle('Session Heart-Rate Over Time', fontsize=14, fontweight='bold')
plot2 = fig.add_subplot(111)
# plot1.set_title('axes title')
plot2.set_xlabel('Time (Seconds)')
plot2.set_ylabel('Heart-Rate (Beats Per Minute)')
fig.set_size_inches(18.5,10.5)
plt.plot(time, bpmGaussSmooth)
plt.axhline(y=80,color='k',ls='dashed')



plt.savefig('saved-plot-gauss.png', dpi = 250)