import numpy as np 
from processing.colors import yiq_to_rgb, to_monochrome
from processing.convolution import convolve

def laplace(img):
  
  laplace = np.array([[0, -1, 0],
                      [-1, 4, -1],
                      [0,-1, 0]])

  if len(img.shape) == 3:
    img = to_monochrome(img)
  else:
    print("aaaaa")
  print(img)
  img = convolve(img, laplace)
  img = np.array(img,dtype=int)
  print(type(img))
  return img
