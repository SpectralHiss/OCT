'''
ADC conversion need to happen at B-Scan level to provide adequate dynamic range.
'''
import numpy as np
import pdb
import matplotlib.pyplot as plt
import math

class ADC:
  def to_img(self,np_b_scan):
    powervals = self.power_spectrum(np_b_scan) 
    return self.grayscale_range_stretch(powervals)
    
  def grayscale_range_stretch(self,np_b_scan):
    minv = np.min(np_b_scan)
    #val_range =  (np_b_scan - .astype('int')
    hist , scale = np.histogram(np_b_scan,256)
    norm_hist = hist / sum(hist)
    cumul_hist = []
    for i,val in enumerate(norm_hist):
      if i >= 1:
        cumul_hist.append(cumul_hist[i-1] + val)
      else:
        cumul_hist = [val]
    eq_img = []
    for pixel in np_b_scan.flatten():
      eq_img.append(math.floor(255 *(cumul_hist[pixel]) + 0.5))

    return np.reshape(np.array(eq_img), (len(np_b_scan),len(np_b_scan[0])))

  def power_spectrum(self,signal):
    return 20 * np.log10(signal * signal , dtype='float32')

'''
def near_scale(pixel,scale):
  idx = (np.abs(scale-pixel)).argmin()
  return idx
'''