#%%
#import matplotlib.pyplot as plt
from time import time
from colors import rgb_to_yiq, yiq_to_rgb
from models import ImageData,MaskData
from operations import convolve, median
#import ops


lena = ImageData('images/lena256color.jpg')
media5 = MaskData('masks/media_3x3.txt')

t0 = time()
ef = convolve(lena, media5)
t1 = time()
print(f"{t1-t0}")
#t0 = time()
#ef = ops.convolve(lena, media5)
#t1 = time()
#print(f"{t1-t0}")

#plt.imshow(ef)
#t0 = time.time()
#for x in range(10):
#  ea = median(ab, size_x=3, size_y=3)

#t1 = time.time(
#plt.imshow(ef.mtx)
#plt.show()



#%%
