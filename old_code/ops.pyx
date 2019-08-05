#cython: language_level=3
import numpy as np
from models import ImageData, MaskData

cimport numpy as np

ctypedef double       npy_float64
ctypedef npy_float64    float64_t
ctypedef unsigned char ubyte

DTYPE = np.int

ctypedef np.int_t DTYPE_t


def convolve(image, mask):
  """ convolve(ImageData,MaskData) -> ImageData, 
  aplica uma máscara convolucional em uma imagem, e retorna a imagem resultante
  """
  #if len(image.mtx.shape) == 2: return mono_convolve(image,mask) #caso monocromático
  
  cdef int img_x,img_y,msk_x, msk_y, lmt_x, lmt_y,x,y, m_y, m_x
  cdef np.ndarray img_proc, arr
  cdef double r = 0.0, g = 0.0, b = 0.0
  
  cdef np.ndarray[ubyte, ndim=3] img = image.mtx
  cdef np.ndarray[double, ndim=2] msk = mask.mtx
  len_y, len_x = img.shape[0], img.shape[1]
  msk_y, msk_x = msk.shape[0], msk.shape[1]

  lim_x, lim_y = msk_x // 2, msk_y // 2
  # criar as bordas e preencher com zeros
  arr = np.zeros((len_y, len_x, 3), dtype=np.float64)

  for y in range(len_y):
    for x in range(len_x):
      #loop interno
      r = 0.0; g = 0.0; b = 0.0
      m_y = 0; m_x = 0

      for y_n in range(y-lim_y, y+lim_y+1):
        if not((y_n < 0) or (y_n >= len_y)): 
          m_x = 0
          for x_n in range(x-lim_x,x+lim_y+1):
            if not((x_n < 0) or (x_n >= len_x)):
              r += img[y_n][x_n][0] * msk[m_y][m_x]
              g += img[y_n][x_n][1] * msk[m_y][m_x]
              b += img[y_n][x_n][2] * msk[m_y][m_x]
            m_x += 1
        m_y += 1
      # salva e clipa
      arr[y][x][0] = 255 if r > 255 else 0 if r < 0 else round(r)
      arr[y][x][1] = 255 if g > 255 else 0 if g < 0 else round(r)
      arr[y][x][2] = 255 if b > 255 else 0 if b < 0 else round(r)

 
  return ImageData(mtx=arr)

