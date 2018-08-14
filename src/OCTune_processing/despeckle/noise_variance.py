from PIL import Image
import pywt
import numpy as np

import pdb

im = Image.open('light-map-10.png')
im = im - np.mean(im)
coefs = pywt.wavedec2(im, 'db4',level=4)

all_vars = []

for lvl_idx,level in enumerate( coefs[1:]):
  new_level = []
  for sub_band in level:
    sub_band_var = []
    sl = np.var(sub_band)  
    new_level.append(sl)
  all_vars+= [new_level]
pdb.set_trace()
np.savetxt('var_noise',all_vars)
print(all_vars)