    
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
        reshape_NAWT_despeckle = reshape.b_scan(0,despeckle='NAWT')

        reshape_Bilateral_despeckle = reshape.b_scan(0,despeckle='bilateral')


        median = reshape.b_scan(0,despeckle='Median')
        fig = plt.figure()
        plt.subplot(151)

        plt.imshow(BScan_orig)
        plt.xlabel('Original B scan')
        plt.subplot(152)
        plt.imshow(reshape_output)
        plt.xlabel('reshape without denoising')
        plt.subplot(153)
        plt.imshow(reshape_NAWT_despeckle)
        plt.xlabel('NAWT denoising denoising')
        plt.subplot(154)
        plt.imshow(reshape_Bilateral_despeckle)
        plt.xlabel('Bilateral denoising')

        plt.subplot(155)
        plt.imshow(median)
        plt.xlabel('Median filtered reconstruction')

        plt.show()
        fig.savefig("./figures/despeckle.png")
        noise_CNR = cnr.CNR(reshape_output)
        median_CNR = cnr.CNR(median)
        bilat_CNR = cnr.CNR(reshape_Bilateral_despeckle)
        nawt_CNR = cnr.CNR(reshape_NAWT_despeckle)
        print("old cnr , median CNR, bilat CNR, NAWT CNR", noise_CNR, median_CNR, bilat_CNR, nawt_CNR)

        