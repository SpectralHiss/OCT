import PIL
from PIL import ImageFilter
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from skimage.filters import scharr 
from skimage import color,morphology
import numpy as np
import pdb

num_segs = 3
DEBUG = False # this draws the segmentation clustering for illustration

def CNR(nparr_img,method=2):
  
  pilimg = PIL.Image.fromarray(nparr_img.astype("float")).convert('RGB')
  im1 = pilimg.filter(ImageFilter.MedianFilter(5))
  
  numpy_img = np.asarray(im1.convert('L'))
  
  p1 = []
  height = len(numpy_img)
  width = len(numpy_img[0])

  for row in range(height):
    for column in range(width):
      if method == 1:
        p1.append([row*0.15,column*0.15,numpy_img[row][column]])
      else:
        p1.append([numpy_img[row][column]])

  #kmeans = KMeans(init=np.array([[np.min(numpy_img)], [int(np.median(numpy_img))],[np.max(numpy_img)]]), n_clusters=num_segs)
  kmeans = KMeans(init='k-means++', n_clusters=num_segs)
  kmeans.fit(p1)

  seg_map = kmeans.labels_.reshape(im1.size[::-1])
  if DEBUG:
    [_,ax] = plt.subplots(1,3)
    ax[0].imshow(color.label2rgb(seg_map,numpy_img))
    ax[1].imshow(scharr(numpy_img))
    ax[2].imshow(numpy_img)
    plt.show()

  regions = [[] for k in range(num_segs)]
  for row in range(len(numpy_img)):
    for col in range(len(numpy_img[0])):
      regions[seg_map[row][col]].append(numpy_img[row][col])

  means = [ np.mean(arr) for arr in regions]
  bg_noise = np.argmin(means)
  fg_hard = np.argmax(means)
  fg_soft = set(range(num_segs)).difference([bg_noise,fg_hard]).pop()
  contrast = (means[fg_hard] - means[fg_soft])
  noise = means[bg_noise]
  if noise == 0:
    CNR = contrast
  else:
    CNR = contrast / noise

  return CNR  