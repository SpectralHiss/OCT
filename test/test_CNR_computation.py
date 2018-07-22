import random
import os
import os.path as path
import PIL
from PIL import ImageFilter

import src.CNR.cnr as cnr
import src.basic_correct.b_scan as bc

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

  BScan_orig = bc.BScan(test_dir).b_scan(0)

  Bscan = BScan_orig * random.random() + random.random() * 255.0

  pilimg = PIL.Image.fromarray(Bscan.astype("float")).convert('RGB')
  im1 = pilimg.filter(ImageFilter.BLUR)
  blurred_CNR = cnr.CNR(np.asarray(im1.convert('LA'))[:,:,0])
  orig_CNR = cnr.CNR(BScan_orig)

  print("CNRS obtained for orig and blurred %3.f %3.f", orig_CNR,blurred_CNR)
  assert(orig_CNR > blurred_CNR)    
