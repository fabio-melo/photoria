#%%
import time
import numpy as np
from utils import check_bounds
from functools import lru_cache

class ConvolutionalMask():
  def __init__(self, file = False):
    self.matrix, self.width, self.height = [],0,0
    self.floor_h, self.floor_w = 0,0

    if file: 
      self.load_from_file(file)
      self.mirror()

  def load_from_file(self,file):
    with open(file,'r') as fl:
      self.matrix = np.array([list(map(float, line.rstrip().split(" "))) \
        for line in fl.readlines()])
      self.height, self.width = self.matrix.shape[0], self.matrix.shape[1]
      self.floor_h, self.floor_w = self.height // 2, self.width // 2
      self.ceil_h, self.ceil_w = self.floor_h + 1, self.floor_w + 1


  def mirror(self):
    self.matrix = np.array([w[::-1] for w in self.matrix[::-1]])


  def apply_on_pixel_dot(self,image,x,y):
    #cria 
    mtx_sl = np.zeros((self.height, self.width, 3))
    #popula 
    for ih, mh in enumerate(range(y - self.floor_h, y + self.ceil_h)):
      if (mh < 0) or (mh >= image.height): continue	
      for iw, mw in enumerate(range(x - self.floor_w, x + self.ceil_w)):
        if (mw < 0) or (mw >= image.width): continue
        mtx_sl[ih][iw] = image.matrix[mh][mw]
    #aplica
    mtx = mtx_sl * self.matrix
    mtx = np.sum(mtx, axis=(0,1))

    return mtx
    
  def fast_apply(self,image):
    mtx = np.zeros((image.matrix.shape))

    t0 = time.time()
    for y in range(self.height,image.height - self.height):
      for x in range(self.width, image.width - self.width):
        res = image.matrix[y-self.floor_h:y+self.ceil_h, x-self.floor_w:x+self.ceil_w] * self.matrix
        mtx[y][x] = np.sum(res,axis=(0,1))

    #CANTOS
    
    for y in range(self.height):
      for x in range(self.width):
        mtx[y][x] = self.apply_on_pixel_dot(image,x,y)

    for y in range(image.height - self.height, image.height):
      for x in range(image.width - self.width, image.width):
        mtx[y][x] = self.apply_on_pixel_dot(image,x,y)
    
    mtx = np.clip(mtx, a_min=0, a_max=255)
    mtx = np.round(mtx)
    mtx = mtx.astype(int)
    
    t1 = time.time()
    print(f"tempo total {t1-t0}")
    return mtx
    

  def apply(self,image):
    mtx = np.zeros((image.matrix.shape))

    t0 = time.time()

    for y in range(image.height):
      for x in range(image.width):
        mtx[y][x] = self.apply_on_pixel_dot(image,x,y)
    
    mtx = np.clip(mtx, a_min=0, a_max=255)
    mtx = np.round(mtx)
    mtx = mtx.astype(int)
    
    t1 = time.time()
    print(f"tempo total {t1-t0}")
    return mtx



from image import ImageMatrix
from median import MedianMask

media = ConvolutionalMask("masks/media_3x3.txt")
gauss = ConvolutionalMask("masks/gauss_3x3.txt")
median = MedianMask()
y = ImageMatrix("images/aaa1.jpg")

media.apply(y)
media.fast_apply(y)

#import matplotlib.pyplot as plt

#_, ax = plt.subplots(2,2)
#ax[0,0].imshow(y.matrix)
#ax[0,1].imshow(media.fast_apply(y))
#ax[1,0].imshow(gauss.fast_apply(y))
#ax[1,1].imshow(median.fast_apply(y))
#plt.show()
#%%



