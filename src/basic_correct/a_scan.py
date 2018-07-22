import numpy as np
from scipy import interpolate
from scipy import fftpack
from scipy import signal
import math
import pdb

import matplotlib.pyplot as plt


def grayscale_range_histogram(nparr):
  pass

class AScan:
  def __init__(self,ref_spectrum,resample,imrange):
    self.ref_spectrum = ref_spectrum
    self.resampling_table = resample
    self.range = imrange

  def deconv_threshold(self,spectrum_val,ref_val):

    if ref_val> 0.1:
      return float(((spectrum_val + 1000.0) / (ref_val + 1000.0)) - 1.0) 
    else:
      return 0.0
    
  def deconv_method(self,spectrum):
    # method by which the source spectrum is deconvolved from IOCT signal
    deconv =  [ self.deconv_threshold(spectrum[i],self.ref_spectrum[i]) for i in range(len(spectrum))]
    #pdb.set_trace()
    
    deconv = deconv - np.mean(deconv)
    #pdb.set_trace()
    
    nuttall = signal.nuttall(1024)
    windowed = [ (deconv[i] * nuttall[i]) for i in range(len(spectrum)) ]
    #pdb.set_trace()
    
    np_deconv = np.array(windowed,dtype='float32')
    #pdb.set_trace()
    
    return np_deconv
  
  def a_scan(self, spectrum):
    np_deconv = self.deconv_method(spectrum)

    spline = interpolate.splrep(np.arange(0,1024), np_deconv, s=0)
    xnew = np.array(self.resampling_table, dtype='float32')
    self.interpolated_spectrum = np.float32(interpolate.splev(xnew,spline))
    return self.correction_method()


  def fftenvelope(self,spectrum):
    positive_complex_freqs = fftpack.fft(spectrum)[0:512]
    # current envelope algo is naive..
    return np.abs(positive_complex_freqs) 

  def clip(self,val):
    if val > 255:
      return 255
    if val <= 0:
      return 0
    else: return int(val)

  def grayscale_range_stretch(self,nparr):
    minv = self.range['min']
    maxv = self.range['max']
  
    span = float(maxv - minv)
    minv = -90
    maxv = minv + span + 10
    #pdb.set_trace()
    return np.array([self.clip(grayscale) for grayscale in ((span/255) * (nparr - minv))], dtype='float32')

  def to_grayscale(self,signal):
    powervals = float(20)* np.log10(signal * signal, dtype='float32')
    out =  self.grayscale_range_stretch(powervals)
    #pdb.set_trace()
    return out

  def correction_method(self):
    signal = self.fftenvelope(self.interpolated_spectrum)
    return self.to_grayscale(signal).astype("int")