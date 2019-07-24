#%%

class ImageMatrix:
	
	def __init__(self, img):
		self.img = img
		self.width = width
		self.height = height

	def get_px(self, y, x):
		if (y < self.height) and (x < self.width) and (y > 0) and (x > 0):
			return self.img[y][x]
		else:
			return (0,0,0)
