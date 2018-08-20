from PIL import Image

from scipy.optimize import curve_fit
  
import matplotlib.pyplot as plt
import scipy.signal as sg
import numpy as np
import math

def func(x, b):
  return np.sinc(9.5 * math.pow(10,-6) *  x) * np.exp(-b * x / (4 * math.log(2))) 

import pdb

light = Image.open('depth-scans/light-map.png')
signal = []

for i in range(512):
  print(i)
  #pdb.set_trace()
  signal.append(light.getpixel((250,i)))

#plt.plot(signal)

peak_i = sg.find_peaks_cwt(signal, np.arange(2,7))
peak_i = peak_i[1:20]
peaks = []

for idx in peak_i:
  peaks.append(signal[idx])

popt, pcov = curve_fit(func, peak_i,peaks,bounds=(0.001,[0.01]))

plt.plot([func(x, popt[0]) for x in range(512)])
plt.show()
inv_coefs = [1/func(val,popt[0]) for val in range(512)]
pdb.set_trace()

np.savetxt('inv_coefs',inv_coefs)
plt.show()