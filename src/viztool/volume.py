import src.conf.conf as conf
import numpy as np

class Volume():
  def __init__(self,dir,bscan_grabber):
    self.conf = conf.Conf(dir)
    self.grabber = bscan_grabber.BScan(dir)

  def get_volume(self):
    #if self.vol_data is None:
    self.vol_data = [ self.grabber.b_scan(n) for n in range(self.conf.numB)]
    return self.vol_data

  def get_np_volume(self):
    # 4D numpy array  (x, y, z, RGBA) with dtype=ubyte.
    # coordinates ...  y!-> x, z up
    # hence each grab is one horizontal layer
    self.get_volume()
    #if self.vol_array is None:
    vol_array = [] #np.array(dtype='ubyte')
    for iz,bscan in enumerate(self.vol_data):
      for iy,scanline in enumerate(bscan):
        for ix,pixel in enumerate(scanline):
          vol_array.append((ix,iy,iz, pixel))
    self.vol_array = vol_array
    return np.array(self.vol_array,dtype='ubyte')
