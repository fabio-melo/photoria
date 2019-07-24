#%%
from numpy import array

class ConvolutionalMask(object):
  def __init__(self, file = False):
    self.matrix, self.width, self.height = [],0,0
    
    if file: 
      self.load_from_file(file)
      self.mirror()

  def load_from_file(self,file):
    with open(file,'r') as fl:
      self.matrix = array([list(map(float, line.rstrip().split(" "))) \
        for line in fl.readlines()])
      self.height, self.width = self.matrix.shape[0], self.matrix.shape[1]

  def mirror(self):
    self.matrix = [w[::-1] for w in self.matrix[::-1]]

x = ConvolutionalMask("masks/1_to_9_3x3.txt")