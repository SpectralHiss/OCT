'''
ADC conversion need to happen at B-Scan level to provide adequate dynamic range.
'''
import numpy as np
import pdb
class ADC:
  def to_img(self,np_b_scan):
    powervals = self.power_spectrum(np_b_scan) 
    return self.grayscale_range_stretch(powervals)
    
  def grayscale_range_stretch(self,np_b_scan):
    minv = np.percentile(np_b_scan,3)
    span = np.percentile(np_b_scan,99) - minv
    stretched = (255 / span * (np_b_scan - minv)).astype('int')
    stretched.clip(0,255,out=stretched)
    return stretched.astype('uint8')

  def power_spectrum(self,signal):
    return 20 * np.log10(signal * signal , dtype='float32')

 