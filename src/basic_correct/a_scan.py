import numpy as np
from scipy import interpolate
from scipy import fftpack
from scipy import signal
import pdb



def grayscale_range_histogram(nparr):
  pass

class AScan:
  def __init__(self,ref_spectrum,resample,imrange):
    self.ref_spectrum = ref_spectrum
    self.resampling_table = resample
    self.range = imrange


  def deconv_method(self,spectrum):
    
    nuttall = signal.nuttall(1024)
    windowed = [ (spectrum[i] * nuttall[i]) for i in range(len(spectrum)) ]
    
    # method by which the source spectrum is deconvolved from IOCT signal
    deconv =  [windowed[i]/self.ref_spectrum[i] for i in range(len(spectrum))]
    
    np_deconv = np.array(deconv)
    return np_deconv - np.mean(np_deconv)
  
  def a_scan(self, spectrum):
    np_deconv = self.deconv_method(spectrum)

    spline = interpolate.splrep(np.arange(0,1024), np_deconv, s=0)
    xnew = np.array(self.resampling_table)
    self.interpolated_spectrum = interpolate.splev(xnew,spline)
    return self.correction_method()

  def fftenvelope(self,spectrum):
    return np.absolute(fftpack.fft(spectrum)[0:512])

  def grayscale_range_stretch(self,nparr):
    minv = self.range['min']
    maxv = self.range['max']
    span = maxv - minv
    #pdb.set_trace()
    return np.array([grayscale for grayscale in ((span/(255)) * (nparr - minv))])

  def to_grayscale(self,signal):
    powervals = 20* np.log(signal * signal)
    return self.grayscale_range_stretch(powervals)

  def correction_method(self):
    signal = self.fftenvelope(self.interpolated_spectrum)
    return self.to_grayscale(signal).astype("int")