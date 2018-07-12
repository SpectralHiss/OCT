import random
import math
import os
import os.path as path
import src.basic_correct.b_scan as bc

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import pdb

class TestBasicB:
  
  data_dir = path.join(os.getcwd() , "../data")

  def read_short(self,f):
    bytes = f.read(2)
    short = int.from_bytes(bytes,byteorder='little')
    return short

  def read_all_spectrums(self,test_dir):
    print(test_dir)
    with open(path.join(test_dir,"Spectra.bin"), 'rb') as f:
      spectrums = []
      # TODO: generalise /refactor
      a_scan_i = 0
      while a_scan_i < 500:
        temp_spectrum = []
        i = 0
        while i < 1024:
          temp_spectrum.append(self.read_short(f))
          i = i +1
        a_scan_i = a_scan_i+1
        spectrums.append(temp_spectrum)
    return spectrums

  def read_first_B_scan(self,a_test_data_dir):
    im = Image.open(path.join(a_test_data_dir,"B-Scans/OCTImage0000.png"))
    px = im.load()
    b_scan = []
    a_scan_i = 0
    while a_scan_i < 500:
      a_scan = ([px[a_scan_i,x][0] for x in range(512)])
      b_scan.append(a_scan)
      a_scan_i = a_scan_i + 1
    return np.transpose(b_scan)

  def within_e_RMSE_IMG(self,desired, actual,e):
    a_index = 0
    r = []
    while a_index < 500:
      r += [ math.pow(actual[a_index][i] - desired[a_index][i],2) for i in range(len(actual[a_index]))]
      a_index +=1
    RMSE = math.sqrt(sum(r))
    print("RMSE",RMSE)
    return RMSE < e

  def test_basic_B_reconstruction(self):
    subdirs = [subdir for subdir in os.listdir(self.data_dir)]
    a_test_data_dir = path.join(self.data_dir,subdirs[int(random.random()* len(subdirs))])

    spectrums = self.read_all_spectrums(a_test_data_dir)

    BScan = bc.BScan(a_test_data_dir)
    out = BScan.b_scan(spectrums)
    desired = self.read_first_B_scan(a_test_data_dir)
    
    assert(len(out) == len(desired))
    assert self.within_e_RMSE_IMG(desired, out,20* 1024 * 500)