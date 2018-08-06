'''
ADC conversion need to happen at B-Scan level to provide adequate dynamic range.
'''
import numpy as np
import pdb
import matplotlib.pyplot as plt

class ADC:
  def to_img(self,np_b_scan):
    powervals = self.power_spectrum(np_b_scan) 
    return self.grayscale_range_stretch(powervals)
    
  def grayscale_range_stretch(self,np_b_scan):

    hist, _ = np.histogram(np_b_scan)
    pdb.set_trace()
    #minv = np.min(np_b_scan)
    minv = -90 # np.min(nparr)
    span = 110
    out = 255 / span * (np_b_scan - minv)
    pdb.set_trace()
    return np.array(out,dtype='int')

  def power_spectrum(self,signal):
    pdb.set_trace()
    return 20 * np.log10(signal * signal , dtype='float32')
