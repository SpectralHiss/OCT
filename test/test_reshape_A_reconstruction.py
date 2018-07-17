import test.test_basic_A_reconstruction as basicmod
import src.spectral_reshaping.a_scan as asc


class TestReshapeA(basicmod.TestBasicA):
  
  def test_reshape_A_reconstruction(self):
    self.test_basic_A_reconstruction(method=asc)