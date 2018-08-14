''' NAWT despeckle method based on : Noise adaptive wavelet thresholding for
speckle noise removal in optical coherence
tomography 2017 Optical Society of America
'''
import pywt

def despeckle(image,ref_image):
  coefs = pywt.wavedec2(image, 'db4',level=4)

  sigma = np.var(range_data)
    
  for lvl_idx,level in enumerate( coefs[2:]):
    new_level = []
      for direction in level:
        new_direction = []
        for row in direction:
          new_row = []
          for i, pixel in enumerate(row):
            new_row += [np.sign(pixel) * np.abs(pixel - 1000 * (math.sqrt(2 * np.log(len(row))) * sigma / math.sqrt(len(row))))]
          new_direction += [new_row]
        new_level += [new_direction]
      coefs[1+lvl_idx] = new_level

    return pywt.waverec2(coefs,'db4')

    #  level[0] #LH
    #  level[1] #HL
    #  level[2] $DD