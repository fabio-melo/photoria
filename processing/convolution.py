import numpy as np



def convolve(img, krn):

	# espelha o kernel	
	# salva os shapes em variaveis
	img_y, img_x = img.shape[0], img.shape[1]
	krn_y, krn_x = krn.shape[0], krn.shape[1]
	lmt_x, lmt_y = krn_x // 2, krn_y // 2

	res = np.zeros(img.shape, dtype=img.dtype) # resultado 
	if len(img.shape) == 2: #monochrome
		img_p = np.pad(img, ((lmt_x,lmt_x),(lmt_y,lmt_y)))
	else:
		img_p = np.pad(img, ((lmt_x,lmt_x),(lmt_y,lmt_y),(0,0)))

	if krn.shape == (3,3) or len(img.shape) == 2:
		for x in range(lmt_x, img_x - lmt_x):
			for y in range(lmt_y, img_y - lmt_y):
				tmp = img_p[y-lmt_y:y+lmt_y+1, x- lmt_x:x+lmt_x+1] * krn
				res[y,x] = np.sum(tmp, axis=(0,1))

	else: # bem mais lento, para kerneis diferentes de 3x3, mas funciona
		for x in range(lmt_x, img_x - lmt_x):
			for y in range(lmt_y, img_y - lmt_y):
				tmp = img_p[y-lmt_y:y+lmt_y+1, x- lmt_x:x+lmt_x+1]
				tmp = [np.squeeze(k) for k in np.dsplit(tmp,3)]
				res[y,x] = np.array([np.sum(k * krn) for k in tmp])

	res = np.round(np.clip(res, a_min=0, a_max=255))


	return res
