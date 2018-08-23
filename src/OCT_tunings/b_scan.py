from .a_scan import AScan as ReshapeAScan
import src.basic_correct.b_scan as bbscan
import src.ADC.contrast_full_range_stretch_ADC as ADC

import numpy as np
import PIL
from PIL import ImageFilter
from PIL import Image
import math

import pywt
import os
import os.path as path

import pdb
class BScan(bbscan.BScan):
  def __init__(self,dir,ADC=ADC.ADC()):
    super(BScan,self).__init__(dir, ADC)

  def save_all_b_scans(self):
    folder='tuned-B-Scan/BScan'
    out_dir = path.join(self.test_dir,folder)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    for num in range(self.conf.numB):
      pil_B_scan = Image.fromarray(self.b_scan(num))
      out_file = path.join(out_dir, str(num)+".png")
      pil_B_scan.save(out_file, 'png')

  def b_scan(self,index,despeckle='NAWT'):
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
    if(despeckle == 'Median'):
      pilimg = PIL.Image.fromarray(image.astype("float")).convert('RGB')
      median_filtered = pilimg.filter(ImageFilter.MedianFilter(5))
      image = np.asarray(median_filtered.convert('L'))
    
    pilimg = PIL.Image.fromarray(image.astype("float")).convert('L')

    numpy_img = np.asarray(pilimg)
    return numpy_img