import random
import math
import os
import os.path as path
import src.basic_correct.correct as bc

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import pdb

data_dir = path.join(os.getcwd() , "../data")

def read_short(f):
  bytes = f.read(2)
  short = int.from_bytes(bytes,byteorder='little')
  return short

def read_first_spectrum(test_dir):
  spectrum = []
  print(test_dir)
  with open(path.join(test_dir,"Spectra.bin"), 'rb') as f:
    i = 0
    while i < 1024:
      spectrum.append(read_short(f))
      i = i +1
  return spectrum

def read_first_A_scan(a_test_data_dir):
  im = Image.open(path.join(a_test_data_dir,"B-Scans/OCTImage0000.png"))
  px = im.load()
  return [px[0,x][0] for x in range(512)]

def within_e_RMSE(desired, actual,e):
  if len(desired) != len(actual):
    return False

  r = [ math.pow(actual[i] - desired[i],2) for i in range(len(actual))]
  print(sum(r))
  return math.sqrt(sum(r)) < e

def test_basic_A_reconstruction():
  subdirs = [subdir for subdir in os.listdir(data_dir)]
  a_test_data_dir = path.join(data_dir,subdirs[int(random.random()* len(subdirs))])

  spectrum = read_first_spectrum(a_test_data_dir)

  c = bc.Correct(a_test_data_dir)
  out = c.a_scan(spectrum)
  desired = read_first_A_scan(a_test_data_dir)
  
  print("correlation #{d}", np.correlate(out,desired)[0])
  assert(len(desired) == 512)
  assert(len(out) == len(desired))
  assert within_e_RMSE(desired, out,100000)
