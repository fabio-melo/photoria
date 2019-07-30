#%%
import numpy as np
import models
from imageio import imread
from numba import autojit



class ImageData():
  """
  Dados de Imagem
  @param file = arquivo da imagem
  """
  def __init__(self, file):
    try: 
      self.matrix = imread(file)
      self.height, self.width = self.matrix.shape[0], self.matrix.shape[1]
    except:
      raise Exception("erro no processamento do arquivo")


class ConvolutionalMask():
  """
  Máscara Convolucional
  @param file = arquivo .txt a se ler com os dados da máscara
  recebe máscaras impares
  """
  def __init__(self, file = False):
    self.matrix, self.width, self.height = [],0,0
    self.floor_h, self.floor_w = 0,0

    if file: 
      self.load_from_file(file)

  def load_from_file(self,file):
    with open(file,'r') as fl:
      self.matrix = np.array([list(map(float, line.rstrip().split(" "))) \
        for line in fl.readlines()])
      self.height, self.width = self.matrix.shape[0], self.matrix.shape[1]
      self.floor_h, self.floor_w = self.height // 2, self.width // 2
      self.ceil_h, self.ceil_w = self.floor_h + 1, self.floor_w + 1
      # convoluciona
      self.matrix = np.array([w[::-1] for w in self.matrix[::-1]])





def convolve(image, mask):
    img,msk = image.matrix, mask.matrix
    img_y, img_x = img.shape[0], img.shape[1]
    msk_y, msk_x = msk.shape[0], msk.shape[1]
    c_chn = img.shape[2]

    #bordas
    
    lmt_x, lmt_y = msk_x // 2, msk_y // 2

    # criar as bordas e preencher com zeros
    img_pd = np.pad(img, ((lmt_x,lmt_x),(lmt_y,lmt_y),(0,0)), mode='constant', constant_values=0)
    r = np.zeros(img.shape, dtype=img.dtype)
    
    # fazer a convolução

    for x in range(lmt_x, img_x - lmt_x):
      for y in range(lmt_y, img_y - lmt_y):
        # extrai a matriz centrada no pivô e convoluciona
        tmp = img_pd[y-lmt_y:y+lmt_y+1, x- lmt_x:x+lmt_x+1] * msk
        r[y][x] = np.sum(tmp,axis=(0,1)) # salva na matriz o resultado da soma, mantendo o eixo RGB

    r = np.round(np.clip(r, a_min=0, a_max=255)) # clipa e arrendonda os limites 
    return r

def median(image, size_y=3, size_x=3):
  img = image.matrix
  img_y, img_x = img.shape[0], img.shape[1]
  med_f = (size_x * size_y) // 2
  print(med_f)
  lmt_x, lmt_y = size_x // 2, size_y // 2
  c_chn = img.shape[2]

  r = np.zeros(img.shape, dtype=img.dtype)
  img_pd = np.pad(img, ((lmt_x,lmt_x),(lmt_y,lmt_y),(0,0)), mode='constant', constant_values=0)


  for x in range(lmt_x, img_x - lmt_x):
    for y in range(lmt_y, img_y - lmt_y):
      tmp = img_pd[y-lmt_y:y+lmt_y+1, x- lmt_x:x+lmt_x+1] 
      arr = np.dsplit(tmp, c_chn)
      r[y][x] = np.array([np.sort(s).flatten()[med_f] for s in arr])
      
  r = np.round(np.clip(r, a_min=0, a_max=255)) # clipa e arrendonda os limites 
  return r







ab = models.ImageData('images/lena256color.jpg')
media = models.ConvolutionalMask('masks/media_3x3.txt')

import matplotlib.pyplot as plt

import time
t0 = time.time()
#ef = convolve(ab, media)
t1 = time.time()
print(f"{t1-t0}")
#plt.imshow(ef)

t0 = time.time()
ea = median(ab, size_x=20, size_y=20)
t1 = time.time()
print(f"{t1-t0}")

plt.imshow(ea)
plt.show()




#

#%%
