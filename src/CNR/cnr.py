import PIL
from PIL import ImageFilter
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from skimage.filters import scharr
from skimage import color,morphology
import numpy as np
import pdb

num_clusters = 4
DEBUG = True

def CNR(nparr_img):
  pilimg = PIL.Image.fromarray(nparr_img.astype("float")).convert('RGB')
  im1 = pilimg.filter(ImageFilter.MedianFilter(15))
  #TODO read adjunct paper and maybe PCA for speed/accuracy?
  numpy_img = np.asarray(im1.convert('L'))[:,:]
  
  p1 = []
  for x in range(len(numpy_img[0])):
    for y in range(len(numpy_img)):
      p1.append([numpy_img[y][x]])#(x,y,numpy_img[y][x]))

  kmeans = KMeans(init='k-means++', n_clusters=num_clusters)
  kmeans.fit(p1)

  out = np.transpose(kmeans.labels_.reshape(im1.size))
  if DEBUG:
    [_,ax] = plt.subplots(2,1)
    ax[0].imshow(color.label2rgb(out,numpy_img))
    ax[1].imshow(scharr(numpy_img))
    plt.show()
    pdb.set_trace()
 

  return 0  