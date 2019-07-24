#%%
from numpy import array, zeros
from utils import check_bounds

class MedianMask():
	def __init__(self, file = False):
		self.matrix, self.width, self.height = [],0,0
		self.floor_h, self.floor_w = 0,0


	def apply_on_pixel(self,image,x,y):
		r_l, g_l, b_l = [],[],[]

		for mh in range(y - self.floor_h, y + self.floor_h + 1):		
			for iw, mw in enumerate(range(x - self.floor_w, x + self.floor_w + 1)):
				if (mh < 0) or (mh >= image.height) or \ 
					(mw < 0) or (mw >= image.width): r_l.append(0),g_l.append(0),b_l.append(0)
				else: 
					r_l.append(image.matrix[mh][mw][0])
					g_l.append(image.matrix[mh][mw][1])
					b_l.append(image.matrix[mh][mw][2])
			
	r_l.sort()
					
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