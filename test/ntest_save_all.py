    
import os
import os.path as path
import random
import pdb
import matplotlib.pyplot as plt
import src.conf.conf as conf
import numpy as np

import test.test_basic_B_reconstruction as basc
import src.basic_correct.b_scan as bc
import src.OCT_tunings.b_scan as rbc

'''Warning this test writes in project dir/out directory

'''

class TestSaveAll():
    
    def test_save_all(self):
        out_data = path.join(os.getcwd() , "../out")

        if not os.path.exists(out_data):
            os.makedirs(out_data)

        #subdirs = [subdir for subdir in os.listdir(data_dir)]
        #subdir = subdirs[int(random.random()* len(subdirs))]
        subdir = 'tooth'
        test_dir = path.join(out_data,subdir)
        proccesing_out_dir = path.join(out_data, 'tooth')
        rbc.BScan(path.join(os.getcwd(),'../data',subdir)).save_all_b_scans(proccesing_out_dir)

        assert(os.path.exists(proccesing_out_dir))
        