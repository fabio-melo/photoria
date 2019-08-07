import numpy as np 
from processing.colors import yiq_to_rgb, to_monochrome_2D, rclip
from processing.convolution import convolve
from math import sqrt


def sobel(img):
  sobel_v = np.array([[ 1,  0, -1],
            [ 2,  0, -2],
            [ 1,  0, -1]])

  sobel_h = np.array([[-1, -2, -1],
            [ 0,  0,  0],
            [ 1,  2,  1]])

  img = to_monochrome_2D(img)
  sv = convolve(img, sobel_v)
  sh = convolve(img, sobel_h)
  sb = np.array([[ sqrt(sv[y,x] **2 + sh[y,x] ** 2) for x in range(img.shape[1])] \
                for y in range(img.shape[0]) ])
  return rclip(sb)