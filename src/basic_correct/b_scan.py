from .a_scan import AScan 
import src.conf.conf as conf
import numpy as np
import os
import os.path as path


def read_short(f):
  bytes = f.read(2)
  short = int.from_bytes(bytes,byteorder='little')
  return short

class BScan():

  def __init__(self, directory):
    self.test_dir = directory
    self.conf = conf.Conf(directory)

  def read_B_spectrums(self,test_dir,index):
    print(test_dir)
    assert(index < self.conf.numB)
    '''
    if(!hasattr(self,spectra_file)):
      self.spectra_file = open(path.join(test_dir,"Spectra.bin"), 'rb')
    '''
    with open(path.join(test_dir,"Spectra.bin"), 'rb') as f:
      f.seek(index * self.conf.B_width * self.conf.spectrum_size)
      spectrums = []
      # TODO: generalise /refactor
      a_scan_i = 0
      while a_scan_i < self.conf.B_width:
        temp_spectrum = []
        i = 0
        while i < self.conf.spectrum_size:
          temp_spectrum.append(read_short(f))
          i = i +1
        a_scan_i = a_scan_i+1
        spectrums.append(temp_spectrum)
    return spectrums

  def b_scan(self,index):
    spectrums = self.read_B_spectrums(self.test_dir,index)
    return np.transpose([AScan(self.conf.ref_spectrum,self.conf.resampling_table,self.conf.range).a_scan(spectrums[i]) for i in range(self.conf.B_width) ])
