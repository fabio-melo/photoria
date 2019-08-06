import os

from processing.loaders import load_image, load_cfilter
from processing.colors import rgb_to_yiq, yiq_to_rgb
from processing.convolution import convolve
from processing.median import median



def mask_list():
	"""retorna a lista de mascaras convolucionais"""
	masks = {}

	for subdir, _, files in os.walk('masks'):
		for file in files:
			filepath = subdir + os.sep + file
			
			if filepath.endswith(".txt"):
				masks[file] = filepath
		
	return masks
				