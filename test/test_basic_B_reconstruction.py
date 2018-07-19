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
  subdirs = [subdir for subdir in os.listdir(data_dir)]
  a_test_data_dir = path.join(data_dir,subdirs[int(random.random()* len(subdirs))])

  def set_data_dir(self,custom_data_dir):
    self.a_test_data_dir = custom_data_dir

  def read_first_B_scan(self,a_test_data_dir):
    im = Image.open(path.join(a_test_data_dir,"B-Scans/OCTImage0000.png"))
    px = im.load()
    self.im_width, _ = im.size
    b_scan = []
    a_scan_i = 0
    while a_scan_i < self.im_width:
      a_scan = ([px[a_scan_i,x][0] for x in range(512)])
      b_scan.append(a_scan)
      a_scan_i = a_scan_i + 1
    return np.transpose(b_scan)

  def within_e_RMSE_IMG(self,desired, actual,e):
    a_index = 0
    r = []
    while a_index < self.im_width:
      r += [ math.pow(actual[a_index][i] - desired[a_index][i],2) for i in range(len(actual[a_index]))]
      a_index +=1
    RMSE = math.sqrt(sum(r))
    print("RMSE",RMSE)
    return RMSE < e

  def test_B_reconstruction(self,method=bc,tolerance=1024):
    desired = self.read_first_B_scan(self.a_test_data_dir)

    BScan = method.BScan(self.a_test_data_dir)
    out = BScan.b_scan(0)
   
    
    assert(len(out) == len(desired))
    assert self.within_e_RMSE_IMG(desired, out,tolerance)