import numpy as np
from imageio import imread

def load_image(file):
	try: 
		img = imread(file)
		return img
	except:
		raise Exception("erro no processamento do arquivo")

def load_cfilter(file):
	try:
		with open(file,'r') as fl:
			krn = np.array([list(map(float, line.rstrip().split(" "))) \
						for line in fl.readlines()])
			#convoluciona  
			krn = np.array([w[::-1] for w in krn[::-1]])
			print(krn)
			return krn
	except:
		raise Exception("erro no processamento do arquivo")  
		
		