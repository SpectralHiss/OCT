import numpy as np
from scipy import interpolate
from scipy import fftpack
from scipy import signal
import math
import pdb

import matplotlib.pyplot as plt

class AScan:
  def __init__(self,ref_spectrum,resample,imrange):
    self.ref_spectrum = ref_spectrum
    self.resampling_table = resample
    self.range = imrange

  def deconv_threshold(self,spectrum_val,ref_val):

    if ref_val> 0.1:
      return float(((spectrum_val + 1000.0) / (ref_val +1000.0)) - 1) 
    else:
      return 0.0
    
  def deconv_method(self,spectrum):
    # method by which the source spectrum is deconvolved from IOCT signa;
    deconv =  [ self.deconv_threshold(spectrum[i],self.ref_spectrum[i]) for i in range(len(spectrum))]
    
    nuttall = signal.blackman(1024)
    windowed = [ (deconv[i] * nuttall[i]) for i in range(len(spectrum)) ]

    deconv = windowed - np.mean(windowed)
    np_deconv = np.array(deconv,dtype='float32')
    
    return np_deconv
  
  def a_scan(self, spectrum):

    #pdb.set_trace()
    np_deconv = self.deconv_method(spectrum)

    spline = interpolate.splrep(np.arange(0,1024), np_deconv, s=0)
    xnew = np.array(self.resampling_table, dtype='float32')
    self.deconv_interpolated_spectrum = np.float32(interpolate.splev(xnew,spline))
    return self.correction_method()


  def range_envelope(self,spectrum):
    positive_complex_freqs = fftpack.fft(spectrum)[1:512]
    return np.abs(positive_complex_freqs)

  def correction_method(self):
    signal = self.range_envelope(self.deconv_interpolated_spectrum)
    return signal