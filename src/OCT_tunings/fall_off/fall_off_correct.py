import numpy as np

import os
import os.path as path

#can be pulled to B scan level for efficiency
def fall_off_correct(np_a_scan):
  inv_coefs = np.loadtxt(path.join(os.path.dirname(__file__),'inv_coefs'))
  for i in range(len(np_a_scan)):
    np_a_scan[i] *= inv_coefs[i]
  return np_a_scan