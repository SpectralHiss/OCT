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


def grayscale_range_stretch(nparr):
  minv = nparr.min()
  maxv = nparr.max()
  return ((255/(maxv - minv)) * (nparr - minv))

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

  def a_scan(self, spectrum):
    deconv =  [spectrum[i]/self.ref_spectrum[i] for i in range(1024)]
    
    np_deconv = np.array(deconv)
    np_deconv = np_deconv - np.mean(np_deconv)

    spline = interpolate.splrep(np.arange(0,1024), np_deconv, s=0)
    xnew = np.array(self.resampling_table)
    self.interpolated_spectrum = interpolate.splev(xnew,spline)
    return self.correction_method()

  def correction_method(self):
    blackman = np.blackman(1024)
    windowed = [ (self.interpolated_spectrum[i] * blackman[i]) for i in range(1024) ]

    powervals = np.absolute(fftpack.fft(windowed)[0:512])
    powervals = 20* np.log(powervals * powervals)
    return grayscale_range_stretch(powervals).astype("int")