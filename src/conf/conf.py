import os
import os.path as path
import csv
import numpy as np

def read_csv_rows_as_array(csv_path):
  with open(csv_path, 'r') as f:
      stream = csv.reader(f, delimiter=',')
      return np.float32([ float(row[1]) for row in stream])

def read_csv_as_dict(csv_path):
  conf = {}
  with open(csv_path,'r') as f:
    stream = csv.reader(f, delimiter=',')
    for row in stream:
      conf[row[0]] = row[1]
  return conf

class Conf:
  def __init__(self,test_dir):
    self.test_dir = test_dir
    self.read_conf()

  def read_conf(self):
    self.read_ref()
    self.read_resampling()
    self.read_range()
    self.read_B_width()
    self.read_num_BScans()
    self.read_spectrum_size()

  def read_spectrum_size(self):
    self.spectrum_size = int(self.param_csv["Spectrum Length"])

  def read_ref(self):
    self.ref_spectrum = read_csv_rows_as_array(path.join(self.test_dir,"referenceSpectrum.csv"))

  def read_resampling(self):
    self.resampling_table = read_csv_rows_as_array(path.join(self.test_dir,"resamplingTable.csv"))

  def read_range(self):
    self.param_csv = read_csv_as_dict(path.join(self.test_dir,"parameters.csv"))
    self.range = {}
    self.range['min'] = float(self.param_csv["Min. Value"]) 
    self.range['max'] = float(self.param_csv["Max. Value"])

  def read_B_width(self):
    self.B_width = int(self.param_csv["Total number of A-Scans per B-Scan"])

  def read_num_BScans(self):
    self.numB = int(self.param_csv["Total number of B-Scans"])