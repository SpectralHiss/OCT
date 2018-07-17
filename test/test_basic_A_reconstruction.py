import random
import math
import os
import os.path as path
import src.basic_correct.a_scan as asc

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import pdb


class TestBasicA:
  data_dir = path.join(os.getcwd() , "../data")

  def read_short(self,f):
    bytes = f.read(2)
    short = int.from_bytes(bytes,byteorder='little')
    return short

  def read_first_spectrum(self,test_dir):
    spectrum = []
    print(test_dir)
    with open(path.join(test_dir,"Spectra.bin"), 'rb') as f:
      i = 0
      while i < 1024:
        spectrum.append(self.read_short(f))
        i = i +1
    return spectrum

  def read_first_A_scan(self,a_test_data_dir):
    im = Image.open(path.join(a_test_data_dir,"B-Scans/OCTImage0000.png"))
    px = im.load()
    return [px[0,x][0] for x in range(512)]

  def within_e_RMSE(self,desired, actual,e):
    if len(desired) != len(actual):
      return False

    r = [ math.pow(actual[i] - desired[i],2) for i in range(len(actual))]
    RMSE = math.sqrt(sum(r))
    print("RMSE",RMSE )
    return RMSE < e

  def test_basic_A_reconstruction(self, method=asc):
    subdirs = [subdir for subdir in os.listdir(self.data_dir)]
    a_test_data_dir = path.join(self.data_dir,subdirs[int(random.random()* len(subdirs))])

    spectrum = self.read_first_spectrum(a_test_data_dir)

    c = method.AScan(a_test_data_dir)
    out = c.a_scan(spectrum)
    desired = self.read_first_A_scan(a_test_data_dir)

    assert(len(desired) == 512)
    assert(len(out) == len(desired))
    assert self.within_e_RMSE(desired, out,20* 1024)
