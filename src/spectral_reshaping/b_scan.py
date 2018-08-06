from .a_scan import AScan as ReshapeAScan
import src.basic_correct.b_scan as bbscan
import numpy as np
import PIL
from PIL import ImageFilter

class BScan(bbscan.BScan):  
  def b_scan(self,index):
    spectrums = self.read_B_spectrums(self.test_dir,index)
    vals =  np.transpose([ReshapeAScan(self.conf.ref_spectrum,self.conf.resampling_table,self.conf.range).a_scan(spectrums[i]) for i in range(self.conf.numB) ])
    pilimg = PIL.Image.fromarray(vals.astype("float")).convert('RGB')
    im1 = pilimg.filter(ImageFilter.SMOOTH)

    numpy_img = np.asarray(im1.convert('L'))
    return numpy_img