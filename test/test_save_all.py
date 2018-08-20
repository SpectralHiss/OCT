    
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
        rbc.BScan(path.join(os.getcwd(),'../data',subdir)).all_b_scans(proccesing_out_dir)

        assert(os.path.exists(proccesing_out_dir))
        '''
        #pdb.set_trace()
        plt.subplot(131)
        plt.imshow(basic_output)
        plt.subplot(132)
        plt.imshow(reshape_output)

        plt.subplot(133)
        plt.imshow(BScan_orig)
        plt.show()
        '''
        #new_CNR = cnr.CNR(reshape_output)
        #old_CNR = cnr.CNR(basic_output)
        #print("old CNR , new CNR", old_CNR, new_CNR)
        #assert(new_CNR > old_CNR)