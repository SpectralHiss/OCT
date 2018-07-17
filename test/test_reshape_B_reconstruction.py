import random
import math
import os
import os.path as path
import src.spectral_reshaping.b_scan as bc
import test.test_basic_B_reconstruction as basicmod

class TestReshapeB(basicmod.TestBasicB):
  
  def test_reshape_B_reconstruction(self):
    self.test_basic_B_reconstruction(method=bc)
