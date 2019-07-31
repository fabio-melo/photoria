import numpy as np
from models import ImageData

def rgb_to_yiq(image):
	img = image.mtx
	img_y, img_x = img.shape[0], img.shape[1]
	
	assert (len(img.shape) == 3)

	r = np.zeros(img.shape, dtype=img.dtype)

	for x in range(img_x):
		for y in range(img_y):
			r,g,b = img[y][x][0],img[y][x][1],img[y][x][2]

			y_ = 0.2989 * r + 0.5870 * g + 0.1140 * b
			i_ = 0.5959 * r - 0.2744 * g - 0.3216 * b
			q_ = 0.2115 * r - 0.5229 * g + 0.3114 * b

			r[y][x] = np.array([y_,i_,q_])
	
	return ImageData(mtx=r)

def yiq_to_rgb(image):
	img = image.mtx
	img_y, img_x = img.shape[0], img.shape[1]
	
	assert (len(img.shape) == 3)

	r = np.zeros(img.shape, dtype=img.dtype)

	for x in range(img_x):
		for y in range(img_y):
			y_,i_,q_ = img[y][x][0],img[y][x][1],img[y][x][2]

			r_ = y_ + 0.9563 * i_ + 0.6210 * q_
			g_ = y_ - 0.2721 * i_ - 0.6474 * q_
			b_ = y_ - 1.1070 * i_ + 1.7046 * q_

			r[y][x] = np.array([r_,g_,b_])
	
	r = np.round(np.clip(r, a_min=0, a_max=255)) # clipa e arrendonda os limites 

	return ImageData(mtx=r)
