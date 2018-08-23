from PIL import Image
import pywt
import numpy as np

import pdb

'''
this script independently reads the light map 10 as a base line for system noise 
since it is a simple mirror reflection at a far distance.
The NAWT method calculate the variance of the 4 level daubechies wvelet and saves them in 
the var_noise variable
'''

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