#%%
import numpy as np
from utils import check_bounds

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
    #cria matriz
    mtx_sl = np.zeros((self.height, self.width, 3))
    #popula matriz
    for ih, mh in enumerate(range(y - self.floor_h, y + self.ceil_h)):
      if (mh < 0) or (mh >= image.height): continue	
      for iw, mw in enumerate(range(x - self.floor_w, x + self.ceil_w)):
        if (mw < 0) or (mw >= image.width): continue
        mtx_sl[ih][iw] = image.matrix[mh][mw]

    #aplica matriz

    mtx = mtx_sl * self.matrix
    mtx = np.sum(mtx, axis=(0,1))
    mtx = np.clip(mtx, a_min=0, a_max=255)
    mtx = np.round(mtx)
    return mtx
    

  def apply(self,image):
    import time
    new = np.zeros((image.matrix.shape))
    
    t0 = time.time()
    for y in range(image.height):
      for x in range(image.width):
        new[y][x] = self.apply_on_pixel_dot(image,x,y)
    t1 = time.time()
    print(f"{t1 - t0}")
    t0 = time.time()

    new = np.array([[self.apply_on_pixel_dot(image,x,y) for x in range(image.width)] for y in range(image.height)])
    t1 = time.time()
    print(f"{t1 - t0}")
    return new





import time
from image import ImageMatrix

x = ConvolutionalMask("masks/media_3x3.txt")
y = ImageMatrix("images/lena256color.jpg")

#t0 = time.time()
niceimg = x.apply(y)
#t1 = time.time()
#print(f"tempo total {t1-t0}")
#print(niceimg)
#import matplotlib.pyplot as plt

#plt.imshow(niceimg)

#%%
