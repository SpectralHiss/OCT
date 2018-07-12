from .test_basic_A_reconstruction import TestBasicA
import src.basic_correct.a_scan as asc


class TestReshapeA(TestBasicA):
  
  def test_reshape_A_reconstruction(self):
    self.test_basic_A_reconstruction(method=asc)
  