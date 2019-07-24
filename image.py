from imageio import imread

class ImageMatrix():
  def __init__(self, file):
    try: 
      self.matrix = imread(file)
      self.height, self.width = self.matrix.shape[0], self.matrix.shape[1]
    except:
      raise Exception("erro no processamento do arquivo")

  def get_px(self, y, x):
    if (y < self.height) and (x < self.width) and (y > 0) and (x > 0):
      return self.img[y][x]
    else: return False
