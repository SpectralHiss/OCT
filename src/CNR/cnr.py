import PIL
from PIL import ImageFilter
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from skimage.filters import sobel
from skimage import color,morphology
import numpy as np
import pdb

num_clusters = 3
DEBUG = True

#TODO: Adjust weights with  Xvalidation?
def CNR(nparr_img,method=2):
  pilimg = PIL.Image.fromarray(nparr_img.astype("float")).convert('RGB')
  im1 = pilimg.filter(ImageFilter.MedianFilter(15))
  #TODO read adjunct paper and maybe PCA for speed/accuracy?
  numpy_img = np.asarray(im1.convert('L'))
  
  p1 = []
  for row in range(len(numpy_img)):
    for column in range(len(numpy_img[0])):
      if method == 1:
        p1.append([x*0.15,y*0.15,numpy_img[x][y]])
      else:
        p1.append([numpy_img[row][column]])

  kmeans = KMeans(init='k-means++', n_clusters=num_clusters)
  kmeans.fit(p1)

  pdb.set_trace()
  out = kmeans.labels_.reshape((im1.size)[::-1])
  if DEBUG:
    [_,ax] = plt.subplots(1,3)
    ax[0].imshow(color.label2rgb(out,numpy_img))
    ax[1].imshow(sobel(numpy_img))
    ax[2].imshow(numpy_img)
    plt.show()
    pdb.set_trace()

  pdb.set_trace()
  return 0  