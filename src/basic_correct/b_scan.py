from .a_scan import AScan 
import numpy as np

class BScan():
    def __init__(self,a_test_data_dir):
      self.test_dir = a_test_data_dir

    def b_scan(self,spectrums):
      return np.transpose([AScan(self.test_dir).a_scan(spectrums[i]) for i in range(len(spectrums)) ])
