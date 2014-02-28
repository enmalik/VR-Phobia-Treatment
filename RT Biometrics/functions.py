import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import spline

from scipy.interpolate import interp1d
from scipy.ndimage import filters
from scipy.signal import gaussian

def singleRunPlot(sessionDir, path, minLine, maxLine, meanLine):
	data = np.loadtxt(path, skiprows=0)

	print data

	time = data[:,2]
	bpm = data[:,3]

	nans, x = nan_helper(bpm)
	bpm[nans]= np.interp(x(nans), x(~nans), bpm[~nans])

	singleRunRawPlot(sessionDir, time, bpm, minLine, maxLine, meanLine)
	singleRunSmoothPlot(sessionDir, time, bpm, minLine, maxLine, meanLine)

	return True


def singleRunRawPlot(sessionDir, time, bpm, minLine, maxLine, meanLine):
	fig = plt.gcf()
	fig.suptitle('Session Heart-Rate Over Time', fontsize=14, fontweight='bold')
	plot1 = fig.add_subplot(111)
	# plot1.set_title('axes title')
	plot1.set_xlabel('Time (Seconds)')
	plot1.set_ylabel('Heart-Rate (Beats Per Minute)')
	fig.set_size_inches(18.5,10.5)
	plt.plot(time, bpm)
	plt.axhline(y = minLine, color = 'orange', ls = 'dashed')
	plt.axhline(y = maxLine, color = 'orange', ls = 'dashed')
	plt.axhline(y = meanLine, color = 'green', ls = 'dashed')
	plt.savefig(sessionDir + 'raw-plot.png', dpi = 250)
	plt.gca().cla()

	print "saved raw plot"

def singleRunSmoothPlot(sessionDir, time, bpm, minLine, maxLine, meanLine):
	numTimes = len(time)
	bpmGaussSmooth = gaussSmooth(bpm, numTimes)
	fig2 = plt.gcf()
	fig2.suptitle('Session Heart-Rate Over Time', fontsize=14, fontweight='bold')
	plot2 = fig2.add_subplot(111)
	# plot1.set_title('axes title')
	plot2.set_xlabel('Time (Seconds)')
	plot2.set_ylabel('Heart-Rate (Beats Per Minute)')
	fig2.set_size_inches(18.5,10.5)
	plt.plot(time, bpmGaussSmooth)
	plt.axhline(y = minLine, color = 'orange', ls = 'dashed')
	plt.axhline(y = maxLine, color = 'orange', ls = 'dashed')
	plt.axhline(y = meanLine, color = 'green', ls = 'dashed')
	plt.savefig(sessionDir + 'smooth-plot.png', dpi = 250)

	print "saved smooth plot"

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

# if __name__ == '__main__':
#     singleRunPlot("writefile.txt", 70, 80, 75)   