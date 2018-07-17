from src.basic_correct.a_scan import AScan
import numpy as np
import math

def bary_interpolation(signal):
  peaks = set([])
  sig_length = len(signal)

  for index,val in enumerate(range(sig_length)[1:-1]):
    if signal[index] > signal[index-1] and signal[index] > signal[index+1]:
      peaks.add(index)

  dz_Os = [ dz_relation(signal[peak-1],signal[peak],signal[peak+1]) for peak in peaks]

  pi = math.pi
  for peaki, peak in enumerate(peaks):
    dz = dz_Os[peaki]
    signal[peak] * ((pi * dz)/ math.sin(pi * dz)) * ((1 - dz * dz) / (0.5 * dz * dz))

  return signal    

def dz_relation(ym_1,ym,ym1):
  # CONSTANT ALERT
  Dz = 9.5 * math.pow(10, -6)
  if ym1 > ym_1:
    return (2 * ym1 - ym) / (ym + ym1)
  else:
    return (ym - 2* ym_1) / (ym + ym_1)  

class AScan(AScan):

  def deconv_method(self,spectrum):
    hann = np.hanning(len(spectrum))
    hann_reshape =  [ hann[i] / self.ref_spectrum[i] for i in range(len(self.ref_spectrum))]

    deconv = [ spectrum[i] * hann_reshape[i] for i in range(len(spectrum)) ]
    return deconv - np.mean(deconv)

  def correction_method(self):
    powervals = self.fftenvelope(self.interpolated_spectrum)
    crisp_signal = bary_interpolation(powervals)
    return self.to_grayscale(crisp_signal).astype("int")
