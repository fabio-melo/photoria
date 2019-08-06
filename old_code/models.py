import numpy as np
from imageio import imread

class ImageData():
  """
  Dados de Imagem
  @param file: arquivo da imagem
  @param mtx: matriz da imagem
  """
  def __init__(self, file=False, mtx=False):
    if file:
      try: 
        self.mtx = imread(file)
        self.height, self.width = self.mtx.shape[0], self.mtx.shape[1]
        self.is_monochrome = True if (len(self.mtx.shape) == 2) else False
       
      except:
        raise Exception("erro no processamento do arquivo")
    elif isinstance(mtx, np.ndarray):
      self.mtx = mtx
    else:
      raise Exception("erro: faltando argumentos - imagedata")


class MaskData():
  """
  Máscara Convolucional
  @param file = arquivo .txt a se ler com os dados da máscara
  recebe (apenas) máscaras impares
  """
  def __init__(self, file = False, mtx=False):
    if file:
      try:
        with open(file,'r') as fl:
          self.mtx = np.array([list(map(float, line.rstrip().split(" "))) \
            for line in fl.readlines()])
      except:
        raise Exception("erro no processamento do arquivo")  
    elif isinstance(mtx, np.ndarray):
      self.mtx = mtx
    else:
      raise Exception("erro: faltam argumentos - convolutionmask")
    #convoluciona  
    self.mtx = np.array([w[::-1] for w in self.mtx[::-1]])

