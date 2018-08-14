from .a_scan import AScan as ReshapeAScan
import src.basic_correct.b_scan as bbscan
import src.ADC.contrast_range_stretch_ADC as ADC

import numpy as np
import PIL
from PIL import ImageFilter
import math

import pywt

import pdb
class BScan(bbscan.BScan):
  def __init__(self,dir):
    super(BScan,self).__init__(dir, ADC.ADC())

  def b_scan(self,index,despeckle=None):
    spectrums = self.read_B_spectrums(self.test_dir,index)
    a_scans = []
    for i in range(self.conf.numB):
      a_scan_i = ReshapeAScan(self.conf.ref_spectrum,self.conf.resampling_table,self.conf.range).a_scan(spectrums[i])
      a_scans.append(a_scan_i)

    range_data =  np.transpose(a_scans)
    image = self.ADC.to_img(range_data)

    if(despeckle == 'NAWT'):
      from .despeckle.wavelet_NAWT_thresold import despeckle
      image = despeckle(image)
    if(despeckle == 'bilateral'):
      from .despeckle.bilateral_filter import despeckle
      image = despeckle(image)
    
    pilimg = PIL.Image.fromarray(image.astype("float")).convert('L')
    #smooth_img = pilimg.filter(ImageFilter.SMOOTH)

    numpy_img = np.asarray(pilimg)
    return numpy_img