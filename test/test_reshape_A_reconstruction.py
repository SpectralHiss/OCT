import test.test_basic_A_reconstruction
import src.spectral_reshaping.a_scan as asc


class TestReshapeA(test.test_basic_A_reconstruction.TestBasicA):
  
  def test_A_reconstruction(self):
    super().test_A_reconstruction(method=asc)