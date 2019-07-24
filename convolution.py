#%%
from numpy import array, zeros
from utils import check_bounds

class ConvolutionalMask():
	def __init__(self, file = False):
		self.matrix, self.width, self.height = [],0,0
		self.floor_h, self.floor_w = 0,0

		if file: 
			self.load_from_file(file)
			self.mirror()

	def load_from_file(self,file):
		with open(file,'r') as fl:
			self.matrix = array([list(map(float, line.rstrip().split(" "))) \
				for line in fl.readlines()])
			self.height, self.width = self.matrix.shape[0], self.matrix.shape[1]
			self.floor_h, self.floor_w = self.height // 2, self.width // 2


	def mirror(self):
		self.matrix = [w[::-1] for w in self.matrix[::-1]]

	def apply_on_pixel(self,image,x,y):
		n_r, n_g, n_b = 0,0,0
		for ih, mh in enumerate(range(y - self.floor_h, y + self.floor_h + 1)):
			if (mh < 0) or (mh >= image.height): continue
				
			for iw, mw in enumerate(range(x - self.floor_w, x + self.floor_w + 1)):
				if (mw < 0) or (mw >= image.width): continue
			
			
				n_r += image.matrix[y][x][0] * self.matrix[ih][iw]
				n_g += image.matrix[y][x][1] * self.matrix[ih][iw]
				n_b += image.matrix[y][x][2] * self.matrix[ih][iw]
		
		if (r < 0): r = 0
		elif (r > 255): r = 255
		if (g < 0): g = 0
		elif (g > 255): g = 255
		if (b < 0): b = 0
		elif (b > 255): b = 255

		return r, g, b

	def apply(self,image):
		new = zeros((image.matrix.shape))
		for y in range(image.height):
			for x in range(image.width):
				new[y][x][0],new[y][x][1],new[y][x][2] = self.apply_on_pixel(image,x,y)

		return new




#%%
