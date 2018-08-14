    
import os
import os.path as path
import random
import pdb
import matplotlib.pyplot as plt
import src.conf.conf as conf
import numpy as np

import test.test_basic_B_reconstruction as basc
import src.basic_correct.b_scan as bc
import src.OCTune_processing.b_scan as rbc
import src.CNR.cnr as cnr

class TestCompareMethods():
    
    def test_side_by_side(self):
        data_dir = path.join(os.getcwd() , "../data")
        subdirs = [subdir for subdir in os.listdir(data_dir)]
        subdir = subdirs[int(random.random()* len(subdirs))]
        subdir = 'tooth'
        test_dir = path.join(data_dir,subdir)

        reshape = rbc.BScan(test_dir)

        BScan_orig = basc.TestBasicB().read_first_B_scan(test_dir)
        reshape_output = reshape.b_scan(0)
        basic_reconstruction = bc.BScan(test_dir)
        basic_output = basic_reconstruction.b_scan(0)
        
        #pdb.set_trace()
        plt.subplot(131)
        plt.imshow(basic_output)
        plt.subplot(132)
        plt.imshow(reshape_output)

        plt.subplot(133)
        plt.imshow(BScan_orig)
        plt.show()

        #new_CNR = cnr.CNR(reshape_output)
        #old_CNR = cnr.CNR(basic_output)
        #print("old CNR , new CNR", old_CNR, new_CNR)
        #assert(new_CNR > old_CNR)