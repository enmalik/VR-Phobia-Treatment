import numpy as np
from scipy.interpolate import spline
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
import numpy

fname = "/Users/nahiyanmalik/Development/VR-Phobia-Treatment/Biometrics/Easy-Pulse/python/timevalue2.txt"

# with open(fname) as f:
#     data = f.readlines()

t, v = [], []

with open(fname) as f:
	for l in f:
	    row = l.split()
	    t.append(row[0])
	    v.append(row[1])

t = map(int, t)
v = map(int, v)

t_np = np.array([t])
v_np = np.array([v])

t_trans = t_np.T
v_trans = v_np.T

print np.shape(t_np)
print np.shape(t_trans)
print np.shape(v_np)
print np.shape(v_trans)

# print t
# print v



xnew = np.linspace(min(t),max(t),300)

value_smooth = spline(t,v,xnew)

maxima = argrelextrema(value_smooth, np.greater)

# print value_smooth

# print maxima

# plt.plot(xnew,value_smooth)
# plt.show()

# print len(v_trans[0])

# def smooth(x,window_len=11,window='hanning'):
#         # if x.ndim != 1:
#         #         raise ValueError, "smooth only accepts 1 dimension arrays."
#         if x.size < window_len:
#                 raise ValueError, "Input vector needs to be bigger than window size."
#         if window_len<3:
#                 return x
#         if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
#                 raise ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"
#         s=numpy.r_[2*x[0]-x[window_len-1::-1],x,2*x[-1]-x[-1:-window_len:-1]]
#         if window == 'flat': #moving average
#                 w=numpy.ones(window_len,'d')
#         else:  
#                 w=eval('numpy.'+window+'(window_len)')
#         y=numpy.convolve(w/w.sum(),s,mode='same')
#         return y[window_len:-window_len+1]


# v_smooth = smooth(v_trans)

'''
Created on Mar 16, 2013

@author: tiago
'''

import numpy as np
from scipy.interpolate import UnivariateSpline
from scipy.signal import wiener, filtfilt, butter, gaussian, freqz
from scipy.ndimage import filters
import scipy.optimize as op
import matplotlib.pyplot as plt

def ssqe(sm, s, npts):
	return np.sqrt(np.sum(np.power(s-sm,2)))/npts

def testGauss(x, y, npts):

	b = gaussian(50, 2)
	#ga = filtfilt(b/b.sum(), [1.0], y)
	ga = filters.convolve1d(y, b/b.sum())
	# plt.plot(x, ga)
	# print "gaerr", ssqe(ga, s, npts)
	return ga

def testButterworth(nyf, x, y, s, npts):
	b, a = butter(4, 1.5/nyf)
	fl = filtfilt(b, a, y)
	plt.plot(x,fl)
	print "flerr", ssqe(fl, s, npts)
	return fl

def testWiener(x, y, s, npts):
	wi = wiener(y, mysize=29, noise=0.5)
	plt.plot(x,wi)
	print "wieerr", ssqe(wi, s, npts)
	return wi

def testSpline(x, y, s, npts):
	sp = UnivariateSpline(x, y, s=240)
	plt.plot(x,sp(x))
	print "splerr", ssqe(sp(x), s, npts)
	return sp(x)

def plotPowerSpectrum(y, w):
	ft = np.fft.rfft(y)
	ps = np.real(ft*np.conj(ft))*np.square(dt)
	plt.plot(w, ps)

npts = 1024
end = 8
dt = end/float(npts)
nyf = 0.5/dt
sigma = 0.5 
# x = np.linspace(0,end,npts)
# r = np.random.normal(scale = sigma, size=(npts))
# s = np.sin(2*np.pi*x)#+np.sin(4*2*np.pi*x)
# y = s + r
# plt.plot(x,s)



# MAKE ON MAXIMA ALGORITHM TO FIX TEH FLAT PARTS

def maxima(vals):
	size = len(vals)
	maxVals = []
	lastVal = 0
	currVal = 0
	incr = 0 # 0 is decr (default), 1 is incr, 2 is flat (currently just using 1)
	flat = 0

	for i in range(size):
		currVal = vals[i]

		if i != 0:
			lastVal = vals[i-1]
			currVal = vals[i]

			rate = currVal - lastVal
			localIncr = 0

			if rate == 0:
				flat = 1
			elif rate < 0:
				localIncr = 0
				flat = 0
			elif rate > 0:
				flat = 0
				localIncr = 1

			if localIncr == 0 and incr == 1 and flat == 0:
				maxVals.append(i-1)
				incr = localIncr
			elif localIncr == 0 and incr == 1 and flat == 1:
				incr = incr
			else:
				incr = localIncr

	return maxVals


x = t
y = v

# plt.plot(x,y,ls='none',marker='.')

yStd = np.std(y);

print "standard deviation: ", yStd

ga = testGauss(x, y, npts)
# fl = testButterworth(nyf, x, y, s, npts)
# wi = testWiener(x, y, s, npts)
# sp = testSpline(x, y, s, npts)

print ga
print len(ga)
print len(v)

maxima_ga = argrelextrema(ga, np.greater)

print len(maxima_ga)
print ga

customMax = maxima(ga)

print "ga maxima: ", maxima_ga
print "custom maxima: ", customMax

# plt.show()
# plt.show(block=True)



plt.plot(x,ga)
plt.show()

