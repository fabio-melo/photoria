#%%
import numpy as np

def rgb_to_yiq(r,g,b):
	
	y = 0.2989 * r + 0.5870 * g + 0.1140 * b
	i = 0.5959 * r - 0.2744 * g - 0.3216 * b
	q = 0.2115 * r - 0.5229 * g + 0.3114 * b

	return y,i,q

def yiq_to_rgb(y,i,q):
	r = round(y + 0.9563 * i + 0.6210 * q)
	g = round(y - 0.2721 * i - 0.6474 * q)
	b = round(y - 1.1070 * i + 1.7046 * q)

	# todas as checagem na mesma linha
	if (r < 0): r = 0
	elif (r > 255): r = 255
	if (g < 0): g = 0
	elif (g > 255): g = 255
	if (b < 0): b = 0
	elif (b > 255): b = 255
	
	return r,g,b

