'''
ADC conversion need to happen at B-Scan level to provide adequate dynamic range.
'''
import numpy as np

class ADC:
  def to_img(self,np_b_scan):
    powervals = self.power_spectrum(np_b_scan) 
    return self.grayscale_range_stretch(powervals)
    
  def grayscale_range_stretch(self,np_b_scan):
    #minv = np.min(np_b_scan)
    minv = -90 # np.min(nparr)
    span = 100
    stretched = span / 255 * (np_b_scan - minv)
    stretched.clip(0,255,out=stretched)
    return stretched.astype('int')

  def power_spectrum(self,signal):
    return 20 * np.log10(signal * signal , dtype='float32')

