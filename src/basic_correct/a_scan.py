import numpy as np
import csv
import os.path as path
from scipy import interpolate
from scipy import fftpack
import pdb

def read_csv_rows_as_array(csv_path):
  with open(csv_path, 'r') as f:
        stream = csv.reader(f, delimiter=',', quotechar='|')
        return [ float(row[1]) for row in stream]



def grayscale_range_histogram(nparr):
  pass

class AScan:
  def __init__(self, directory):
    self.directory = directory
    self.read_ref()
    self.read_resampling()

  def read_ref(self):
    self.ref_spectrum = read_csv_rows_as_array(path.join(self.directory,"referenceSpectrum.csv"))

  def read_resampling(self):
    self.resampling_table = read_csv_rows_as_array(path.join(self.directory,"resamplingTable.csv"))

  #TODO: find better refactor
  def deconv_method(self,spectrum):
    blackman = np.blackman(1024)
    windowed = [ (spectrum[i] * blackman[i]) for i in range(len(spectrum)) ]

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

  #TODO: move in
  def grayscale_range_stretch(self,nparr):
    minv = nparr.min()
    maxv = nparr.max()
    return ((255/(maxv - minv)) * (nparr - minv))

  def to_grayscale(self,signal):
    powervals = 20* np.log(signal * signal)
    return self.grayscale_range_stretch(powervals)

  def correction_method(self):
    signal = self.fftenvelope(self.interpolated_spectrum)
    return self.to_grayscale(signal).astype("int")