import numpy as np
import nrrd
import volume
import os
import os.path as path
import random
import pdb
import matplotlib.pyplot as plt
import numpy as np

import pdb
import src.basic_correct.b_scan as rbc

data_dir = path.join(os.getcwd() , "data")
subdirs = [subdir for subdir in os.listdir(data_dir)]
#subdir = subdirs[int(random.random()* len(subdirs))]
subdir = 'tooth'
test_dir = path.join(data_dir,subdir)

filename = 'testdata.nrrd'

# write to a nrrd file

pdb.set_trace()

nrrd.write(filename, volume.Volume(test_dir,rbc).get_np_volume())