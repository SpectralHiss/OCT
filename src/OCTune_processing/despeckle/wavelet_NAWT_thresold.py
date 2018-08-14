''' NAWT despeckle method based on : Noise adaptive wavelet thresholding for
speckle noise removal in optical coherence
tomography 2017 Optical Society of America

Although it seemed promising to use a variable threshold for each level of variational
and trend encoding embedded in wavelet transform, it oddly did not have any effect..
This method needs tuning with a phantom and perhaps the base noise level is inadequate
the improvements boasted in paper are not that drastic..
This did not work.. welcome to try and improve it..
'''
import pywt
import math
import numpy as np
import os
import os.path as path
import pdb

def despeckle(image):

  mean_image = image - np.mean(image)

  coefs = pywt.wavedec2(mean_image, 'db4',level=4)

  noise_variance = np.median(np.abs(coefs[1][0])) / 0.6745
  
  level_noise = np.loadtxt(path.join(os.path.dirname(__file__),'var_noise'))
  
  signal_band_vars = []
  
  for lvl_idx,level in enumerate( coefs[1:]):
    new_level = []
    for sub_band in level:
      sub_band_var = []
      sl = np.var(sub_band)  
      new_level.append(sl)
    signal_band_vars+= [new_level]

  thresholds = []
  for lvl_i, lvl in enumerate(level_noise):
    level_subband_thresholds = []
    for band_i, band in enumerate(level_noise[lvl_i]):
      level_subband_thresholds.append(level_noise[lvl_i][band_i]*10/math.sqrt(np.max(signal_band_vars[lvl_i][band_i] - noise_variance,0)))
    thresholds.append(level_subband_thresholds)

  real_image = pywt.wavedec2(image, 'db4',level=4)
  
  for lvl_idx,level in enumerate( real_image[1:]):
    new_level = []
    for dir_idx, direction in enumerate(level):
      new_direction = []
      for row in direction:
        new_row = []
        for i, pixel in enumerate(row):
          abs_pixel = np.abs(pixel)
          threshold = thresholds[lvl_idx][dir_idx]
          if(abs_pixel > threshold):
            new_row += [np.sign(pixel) * np.abs(pixel - threshold)]
          else:
            new_row += [0]
        new_direction += [new_row]
      new_level += [new_direction]
      real_image[1+lvl_idx] = new_level

    return pywt.waverec2(real_image,'db4')
    
    #  level[0] #LH
    #  level[1] #HL
    #  level[2] $DD