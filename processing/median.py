import numpy as np

def median(img, krn_y=3, krn_x=3):
	"""Median(ImageData, size_y=int, size_x=int) -> ImageData()
	aplica uma máscara mediana de tamanho size_x X size_y na imagem, e 
	retorna a imagem resultante
	"""
	
	res = np.zeros(img.shape, dtype=img.dtype)
	img_y, img_x = img.shape[0], img.shape[1]
	lmt_x, lmt_y = krn_x // 2, krn_y // 2
	med_f = (krn_x * krn_y) // 2
	
	if len(img.shape) == 2: # mono
		img_p = np.pad(img, ((lmt_x,lmt_x),(lmt_y,lmt_y)))
		
		for x in range(lmt_x, img_x - lmt_x):
			for y in range(lmt_y, img_y - lmt_y):
				tmp = img_p[y-lmt_y:y+lmt_y+1, x- lmt_x:x+lmt_x+1]
				tmp = np.sort(tmp, axis=None) 
				res[y,x] = tmp[med_f]
	else: #color
		img_p = np.pad(img, ((lmt_x,lmt_x),(lmt_y,lmt_y),(0,0)))
		img_r, img_g, img_b = np.dsplit(img_p, 3)

		for x in range(lmt_x, img_x - lmt_x):
			for y in range(lmt_y, img_y - lmt_y):
				tmp_r = (np.sort(img_r[y-lmt_y:y+lmt_y+1, x- lmt_x:x+lmt_x+1], axis=None))[med_f]
				tmp_g = (np.sort(img_g[y-lmt_y:y+lmt_y+1, x- lmt_x:x+lmt_x+1], axis=None))[med_f]
				tmp_b = (np.sort(img_b[y-lmt_y:y+lmt_y+1, x- lmt_x:x+lmt_x+1], axis=None))[med_f]
				res[y,x] = [tmp_r, tmp_g, tmp_b]


	res = np.round(np.clip(res, a_min=0, a_max=255)) # clipa e arrendonda os limites 
	return res