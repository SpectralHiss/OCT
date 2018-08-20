    
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
import src.ADC.contrast_full_range_stretch_ADC as crange_ADC
import src.ADC.contrast_stretch_ADC as const_stretch_ADC

class TestCompareMethods():
    
    def test_side_by_side(self):
        data_dir = path.join(os.getcwd() , "../data")
        subdirs = [subdir for subdir in os.listdir(data_dir)]
        subdir = subdirs[int(random.random()* len(subdirs))]
        subdir = 'tooth'
        test_dir = path.join(data_dir,subdir)

        bc_scan_grabber = bc.BScan(test_dir,ADC=const_stretch_ADC.ADC())

        reshape_crange = rbc.BScan(test_dir,ADC=crange_ADC.ADC())

        BScan_orig = basc.TestBasicB().read_first_B_scan(test_dir)
        
        basic_output_c_stretch = bc_scan_grabber.b_scan(0)

        reshape_output_c_range = reshape_crange.b_scan(0,despeckle=None)
        
        plt.title('Comparison between previous reconstruction, port and our method')
        plt.subplot(131)
        plt.imshow(BScan_orig)
        plt.xlabel('The previous iteration of computational backend')
        plt.subplot(132)
        plt.imshow(basic_output_c_stretch)
        plt.xlabel('Our ported version of the code')
        plt.subplot(133)
        plt.imshow(reshape_output_c_range)
        plt.xlabel('Our denoised spectral and fall-off corrected reconstruction')
        plt.show()

        new_CNR = cnr.CNR(reshape_output_c_range)
        old_CNR = cnr.CNR(basic_output_c_stretch)
        print("old CNR , new CNR", old_CNR, new_CNR)
        assert(new_CNR > old_CNR)