#%%
import numpy as np
from models import ImageData,MaskData


def convolve(image, mask):
  """ convolve(ImageData,MaskData) -> ImageData, 
  aplica uma máscara convolucional em uma imagem, e retorna a imagem resultante
  """
  if len(image.mtx.shape) == 2: return mono_convolve(image,mask) #caso monocromático
  
  img,msk = image.mtx, mask.mtx
  img_y, img_x = img.shape[0], img.shape[1]
  msk_y, msk_x = msk.shape[0], msk.shape[1]
  c_chn = img.shape[2]
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
  return ImageData(mtx=r)

def mono_convolve(image,mask):
  """ mono_convolve(ImageData,MaskData) -> ImageData, 
  aplica uma máscara convolucional em uma imagem monocromática, 
  e retorna a imagem resultante
  """
  img,msk = image.mtx, mask.mtx
  img_y, img_x = img.shape[0], img.shape[1]
  msk_y, msk_x = msk.shape[0], msk.shape[1]
  lmt_x, lmt_y = msk_x // 2, msk_y // 2

  # criar as bordas e preencher com zeros
  img_pd = np.pad(img, ((lmt_x,lmt_x),(lmt_y,lmt_y)), mode='constant', constant_values=0)
  r = np.zeros(img.shape, dtype=img.dtype) #vetor resultado
  
  # fazer a convolução
  for x in range(lmt_x, img_x - lmt_x):
    for y in range(lmt_y, img_y - lmt_y):
      r[y][x] = np.sum(img_pd[y-lmt_y:y+lmt_y+1, x- lmt_x:x+lmt_x+1] * msk)

  r = np.round(np.clip(r, a_min=0, a_max=255)) # clipa e arrendonda os limites 
  return ImageData(mtx=r)



def median(image, size_y=3, size_x=3):
  """Median(ImageData, size_y=int, size_x=int) -> ImageData()
  aplica uma máscara mediana de tamanho size_x X size_y na imagem, e 
  retorna a imagem resultante
  """
  img = image.mtx
  if len(img.shape) == 2: img = np.expand_dims(img, axis=2) # monochrome
  img_y, img_x = img.shape[0], img.shape[1]
  med_f = (size_x * size_y) // 2
  lmt_x, lmt_y = size_x // 2, size_y // 2
  c_chn = img.shape[2]

  r = np.zeros(img.shape, dtype=img.dtype)
  img_pd = np.pad(img, ((lmt_x,lmt_x),(lmt_y,lmt_y),(0,0)), mode='constant', constant_values=0)


  for x in range(lmt_x, img_x - lmt_x):
    for y in range(lmt_y, img_y - lmt_y):
      tmp = img_pd[y-lmt_y:y+lmt_y+1, x- lmt_x:x+lmt_x+1] 
      arr = np.dsplit(tmp, c_chn)
      r[y][x] = np.array([np.sort(s).flatten()[med_f] for s in arr])

  if c_chn == 1: r = np.squeeze(r) #tratar monocromático   
  r = np.round(np.clip(r, a_min=0, a_max=255)) # clipa e arrendonda os limites 
  return ImageData(mtx=r)


#%%
