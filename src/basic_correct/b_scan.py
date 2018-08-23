from .a_scan import AScan 
import src.conf.conf as conf
import src.ADC.contrast_stretch_ADC as ADC
import numpy as np
import os
import os.path as path


def read_short(f):
  bytes = f.read(2)
  short = int.from_bytes(bytes,byteorder='little')
  return short

class BScan():

  def __init__(self, directory,ADC=ADC.ADC()):
    self.test_dir = directory
    self.conf = conf.Conf(directory)
    self.ADC = ADC

  def save_all_b_scans(self,folder='Basic/BScan'):
    out_dir = path.join(self.test_dir,folder)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    for num in range(self.conf.numB):
      pil_B_scan = Image.fromarray(self.b_scan(num))
      out_file = path.join(out_dir, str(num)+".png")
      pil_B_scan.save(out_file, 'png')

  def read_B_spectrums(self,test_dir,index):
    print(test_dir)
    assert(index < self.conf.numB)

    with open(path.join(test_dir,"Spectra.bin"), 'rb') as f:
      f.seek(index * self.conf.B_width * self.conf.spectrum_size * 2) # reading in 16 bits = 2bytes
      spectrums = []
      # TODO: generalise /refactor
      a_scan_i = 0
      while a_scan_i < self.conf.B_width:
        temp_spectrum = []
        i = 0
        while i < self.conf.spectrum_size:
          temp_spectrum.append(read_short(f))
          i = i +1
        a_scan_i = a_scan_i+1
        spectrums.append(temp_spectrum)
    return spectrums

  def b_scan(self,index):
    spectrums = self.read_B_spectrums(self.test_dir,index)
    range_data = np.transpose([AScan(self.conf.ref_spectrum,self.conf.resampling_table,self.conf.range).a_scan(spectrums[i]) for i in range(self.conf.B_width) ])
    img = self.ADC.to_img(range_data)
    return img