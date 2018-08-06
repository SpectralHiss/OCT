from .a_scan import AScan as ReshapeAScan
import src.basic_correct.b_scan as bbscan
import src.ADC.histo_eq_stretch_ADC as ADC

import numpy as np
import PIL
from PIL import ImageFilter

class BScan(bbscan.BScan):
  def __init__(self,dir):
    super(BScan,self).__init__(dir, ADC.ADC())

  def b_scan(self,index):
    spectrums = self.read_B_spectrums(self.test_dir,index)
    range_data =  np.transpose([ReshapeAScan(self.conf.ref_spectrum,self.conf.resampling_table,self.conf.range).a_scan(spectrums[i]) for i in range(self.conf.numB) ])
    image = self.ADC.to_img(range_data)
    pilimg = PIL.Image.fromarray(image.astype("float")).convert('RGB')
    smooth_img = pilimg.filter(ImageFilter.SMOOTH)

    numpy_img = np.asarray(smooth_img.convert('L'))
    return numpy_img