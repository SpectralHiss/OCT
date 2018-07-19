import test.test_basic_B_reconstruction as basc
import PIL
from PIL import ImageFilter
import src.CNR.cnr
from scipy import fftpack
import math
import random
import os
import os.path as path
import src.CNR.cnr as cnr


import numpy as np
import pdb
import matplotlib.pyplot as plt


# SANITY CHECK: blur and add noise to image and see CNR reduced
def test_CNR_computation():
  data_dir = path.join(os.getcwd() , "../data")
  subdirs = [subdir for subdir in os.listdir(data_dir)]
  #subdir = subdirs[int(random.random()* len(subdirs))]
  subdir = 'tooth'
  test_dir = path.join(data_dir,subdir)

  BScan_orig = basc.TestBasicB().read_first_B_scan(test_dir)
  print(cnr.CNR(BScan_orig))

  Bscan = BScan_orig * random.random() + random.random() * 255.0

  pilimg = PIL.Image.fromarray(Bscan.astype("float")).convert('RGB')
  im1 = pilimg.filter(ImageFilter.BLUR)
  assert(cnr.CNR(np.asarray(im1.convert('LA'))[:,:,0])  < cnr.CNR(BScan_orig))