from .a_scan import AScan 
import numpy as np
import os
import os.path as path
import csv

def read_csv_rows_as_array(csv_path):
  with open(csv_path, 'r') as f:
      stream = csv.reader(f, delimiter=',')
      return [ float(row[1]) for row in stream]

def read_csv_as_dict(csv_path):
  conf = {}
  with open(csv_path,'r') as f:
    stream = csv.reader(f, delimiter=',')
    for row in stream:
      conf[row[0]] = row[1]

  return conf

def read_short(f):
  bytes = f.read(2)
  short = int.from_bytes(bytes,byteorder='little')
  return short

class BScan():

  def __init__(self, directory):
    self.test_dir = directory
    self.read_conf()

  def read_conf(self):
    self.read_ref()
    self.read_resampling()
    self.read_range()
    self.read_B_width()
    self.read_num_BScans()
    self.read_spectrum_size()

  def read_spectrum_size(self):
    self.spectrum_size = int(self.conf["Spectrum Length"])

  def read_ref(self):
    self.ref_spectrum = read_csv_rows_as_array(path.join(self.test_dir,"referenceSpectrum.csv"))

  def read_resampling(self):
    self.resampling_table = read_csv_rows_as_array(path.join(self.test_dir,"resamplingTable.csv"))

  def read_range(self):
    self.conf = read_csv_as_dict(path.join(self.test_dir,"parameters.csv"))
    self.range = {}
    self.range['min'] = int(self.conf["Min. Value"]) 
    self.range['max'] = int(self.conf["Max. Value"])

  def read_B_width(self):
    self.B_width = int(self.conf["Total number of A-Scans per B-Scan"])

  def read_num_BScans(self):
    self.numB = int(self.conf["Total number of B-Scans"])

  def read_B_spectrums(self,test_dir,index):
    print(test_dir)
    assert(index < self.numB)

    with open(path.join(test_dir,"Spectra.bin"), 'rb') as f:
      f.seek(index * self.B_width * self.spectrum_size)
      spectrums = []
      # TODO: generalise /refactor
      a_scan_i = 0
      while a_scan_i < self.B_width:
        temp_spectrum = []
        i = 0
        while i < self.spectrum_size:
          temp_spectrum.append(read_short(f))
          i = i +1
        a_scan_i = a_scan_i+1
        spectrums.append(temp_spectrum)
    return spectrums

  def b_scan(self,index):
    spectrums = self.read_B_spectrums(self.test_dir,0)
    return np.transpose([AScan(self.ref_spectrum,self.resampling_table,self.range).a_scan(spectrums[i]) for i in range(self.numB) ])
