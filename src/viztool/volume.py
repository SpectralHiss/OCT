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
    vol_absica = []
    #if self.vol_array is None:
    for iz,bscan in enumerate(self.vol_data):
      vol_ordonne = []
      for iy,scanline in enumerate(bscan):
        vol_cote = [] #np.array(dtype='ubyte')
        for ix,pixel in enumerate(scanline):
          vol_cote.append(pixel)
        vol_ordonne.append(vol_cote)
    vol_absica.append(vol_ordonne)
    self.vol_array = vol_absica
    return np.array(self.vol_array,dtype='ubyte')
