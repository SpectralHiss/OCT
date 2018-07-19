import test.test_basic_B_reconstruction as basc
import src.basic_correct.b_scan as bc
import src.spectral_reshaping.b_scan as asc
import os
import os.path as path
import random
import pdb
import matplotlib.pyplot as plt

class TestCompareMethods():
    
    def test_side_by_side(self):
        data_dir = path.join(os.getcwd() , "../data")
        subdirs = [subdir for subdir in os.listdir(data_dir)]
        #subdir = subdirs[int(random.random()* len(subdirs))]
        subdir = 'tooth'
        test_dir = path.join(data_dir,subdir)


        BScan2 = asc.BScan(test_dir)
 

        BScan_orig = basc.TestBasicB().read_first_B_scan(test_dir)

        spectrums = basc.TestBasicB().read_all_first_spectrums(test_dir)

        out2 = BScan2.b_scan(spectrums)
        BScan = bc.BScan(test_dir)
        out1 = BScan.b_scan(spectrums)


        plt.subplot(131)
        plt.imshow(out1)
        plt.subplot(132)
        plt.imshow(out2)

        plt.subplot(133)
        plt.imshow(BScan_orig)
        plt.show()