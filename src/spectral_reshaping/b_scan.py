from .a_scan import AScan as ReshapeAScan
import src.basic_correct.b_scan as bbscan
import numpy as np

class BScan(bbscan.BScan):  
  def b_scan(self,index):
    spectrums = self.read_B_spectrums(self.test_dir,0)
    return np.transpose([ReshapeAScan(self.conf.ref_spectrum,self.conf.resampling_table,self.conf.range).a_scan(spectrums[i]) for i in range(self.conf.numB) ])
