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


if __name__ == '__main__':
  rgb_yiq_test()

#%%
