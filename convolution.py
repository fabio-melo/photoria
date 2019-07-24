#%%
from numpy import array

class ConvolutionalMask(object):
  def __init__(self, file = False):
    self.matrix = []
    self.width = 0
    self.height = 0
    
    if file: 
      self.load_from_file(file)
      self.mirror()


  def load_from_file(self,file):
    mtx = []
    with open(file,'r') as fl:
      for line in fl.readlines():
        mtx.append(list(map(float, line.rstrip().split(" "))))
    
    self.matrix = array(mtx)
    self.height = self.matrix.shape[0]
    self.width = self.matrix.shape[1]


  def mirror(self):
    #mtx = [[self.matrix[h][w] for w in range(self.width-1, -1, -1)] for h in range(self.height-1,-1,-1)]
    mtx =[w[::-1] for w in self.matrix[::-1]]
   
    """
    mtx = []
    for h in range(self.height -1, -1, -1):
      row = []
      for w in range(self.width -1, -1, -1):
        row.append(self.matrix[h][w])
      mtx.append(row)
    """
    self.matrix = array(mtx)

    print(self.matrix)

x = ConvolutionalMask("masks/1_to_9_3x3.txt")
#%%
