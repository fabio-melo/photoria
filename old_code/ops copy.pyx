#cython: language_level=3
import numpy as np
from models import ImageData, MaskData

cimport numpy as np

DTYPE = np.float

def convolve(image, mask):
  """ convolve(ImageData,MaskData) -> ImageData, 
  aplica uma máscara convolucional em uma imagem, e retorna a imagem resultante
  """
  #if len(image.mtx.shape) == 2: return mono_convolve(image,mask) #caso monocromático
  
  cdef int img_x,img_y,msk_x, msk_y, lmt_x, lmt_y,x,y, m_y, m_x
  cdef np.ndarray img_proc, arr
  cdef float r = 0.0, g = 0.0, b = 0.0
  
  img,msk = image.mtx, mask.mtx
  img_y, img_x = img.shape[0], img.shape[1]
  msk_y, msk_x = msk.shape[0], msk.shape[1]

  lmt_x, lmt_y = msk_x // 2, msk_y // 2

  # criar as bordas e preencher com zeros
  img_proc = np.pad(img, ((lmt_x,lmt_x),(lmt_y,lmt_y),(0,0)), mode='constant', constant_values=0)
  arr = np.zeros(img.shape, dtype=DTYPE)

  
  for x in range(lmt_x, img_x - lmt_x):
    for y in range(lmt_y, img_y - lmt_y):
    #loop interno
      r = 0.0; g = 0.0; b = 0.0
      m_y = 0; m_x = 0
      
      for y_n in range(y-lmt_y,y+lmt_y+1):
        for x_n in range(x-lmt_x,x+lmt_x+1):
          r += img_proc[y_n][x_n][0] * msk[m_y][m_x]
          g += img_proc[y_n][x_n][1] * msk[m_y][m_x]
          b += img_proc[y_n][x_n][2] * msk[m_y][m_x]
          print(f"{img_proc[y_n][x_n]} A")
          m_x += 1
        m_y += 1
      
      arr[y][x][0] = r
      arr[y][x][1] = g
      arr[y][x][2] = b


  arr = np.round(np.clip(arr, a_min=0, a_max=255)) # clipa e arrendonda os limites 
  return ImageData(mtx=arr)

