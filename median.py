#%%
import numpy as np
import time

class MedianMask():
  def __init__(self):
    self.matrix, self.width, self.height = [],0,0
    self.floor_h, self.floor_w = 0,0


  def apply_on_pixel(self,image,x,y):
    r_l, g_l, b_l = [],[],[]

    for mh in range(y - self.floor_h, y + self.floor_h + 1):		
      for iw, mw in enumerate(range(x - self.floor_w, x + self.floor_w + 1)):
        if (mh < 0) or (mh >= image.height) or (mw < 0) or (mw >= image.width): 
          r_l.append(0),g_l.append(0),b_l.append(0)
        else: 
          r_l.append(image.matrix[mh][mw][0])
          g_l.append(image.matrix[mh][mw][1])
          b_l.append(image.matrix[mh][mw][2])
      
    r = sorted(r_l)[len(r_l) // 2]
    g = sorted(g_l)[len(g_l) // 2]
    b = sorted(b_l)[len(b_l) // 2]
        
    return r, g, b

  def apply(self,image):
    mtx = np.zeros((image.matrix.shape))

    t0 = time.time()

    for y in range(image.height):
      for x in range(image.width):
        mtx[y][x] = self.apply_on_pixel(image,x,y)
    
    mtx = np.clip(mtx, a_min=0, a_max=255)
    mtx = np.round(mtx)
    mtx = mtx.astype(int)
    
    t1 = time.time()
    print(f"tempo total {t1-t0}")
    return mtx