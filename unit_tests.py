#%%	
# test_functions
def rgb_yiq_test():
  from rgb_yiq import rgb_to_yiq, yiq_to_rgb
  for r in range(256):
    for g in range(256):
      for b in range(256):
        y ,i ,q  = rgb_to_yiq(r,g,b)
        r1,g1,b1 = yiq_to_rgb(y,i,q)
        assert (r == r1) and (g == g1) and (b == b1)
  print("RGB_YIQ TEST PASSED!")




#%%

from convolution import ConvolutionalMask
from image import ImageMatrix
from median import MedianMask

media = ConvolutionalMask("masks/media_3x3.txt")
gauss = ConvolutionalMask("masks/gauss_3x3.txt")
median = MedianMask()
y = ImageMatrix("images/aaa1.jpg")


import matplotlib.pyplot as plt

_, ax = plt.subplots(2,2)
ax[0,0].imshow(y.matrix)
ax[0,1].imshow(media.apply(y))
ax[1,0].imshow(gauss.apply(y))
ax[1,1].imshow(median.apply(y))
plt.show()
#%%
