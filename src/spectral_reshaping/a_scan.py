from src.basic_correct.a_scan import AScan
import numpy as np
import math
import pdb
from scipy import signal as signal_lib

import matplotlib.pyplot as plt

def bary_interpolation(signal):
  peaks = []
  sig_length = len(signal)
  
  for index in range(sig_length)[1:-1]:
    if signal[index] > signal[index-1] and signal[index] > signal[index+1]:
      if(signal[index] > 0.2):
        peaks.append(index)
  
  dz_Os = [ dz_relation(signal[peak-1],signal[peak],signal[peak+1]) for peak in peaks]
  pi = math.pi
  for peaki, peak in enumerate(peaks):
    dz = dz_Os[peaki]
    signal[peak] = signal[peak] * ((2 * pi * dz)/ math.sin(pi * dz)) * ((1 - dz * dz) )# / (0.5 * dz * dz))
  return signal    

def dz_relation(ym_1,ym,ym1):
  # CONSTANT ALERT
  Dz = (9.5 * math.pow(10, -6))
  if ym1 > ym_1:
    return (2 * ym1 - ym) / (ym + ym1) * Dz
  else:
    return (ym - 2* ym_1) / (ym + ym_1) * Dz

class AScan(AScan):
  
  def grayscale_range_stretch(self,nparr):
    hist,_ = np.histogram(nparr,1000)
    minv = -90 # np.min(nparr)
    maxv = 10
    span = 110
    out = np.array([self.clip(grayscale) for grayscale in ((span/255) * (nparr - minv ))], dtype='int')
    #pdb.set_trace()
    return out

  def deconv_method(self,spectrum):
    hann = np.hanning(len(spectrum))
    hann_reshape =  [ hann[i] / self.ref_spectrum[i] for i in range(len(self.ref_spectrum))]
    deconv = [ spectrum[i] * hann_reshape[i] for i in range(len(spectrum)) ]

    return deconv

  def correction_method(self):
    powervals = self.fftenvelope(self.deconv_interpolated_spectrum)
    crisp_signal = bary_interpolation(powervals)
    return self.to_grayscale(crisp_signal).astype("int")
