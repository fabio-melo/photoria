import numpy as np

# Uteis
def rclip(img):
  # modo artesanal
  return np.round(np.clip(img, a_min=0,a_max=255))

def rgb_to_yiq(img):
  return np.array([[[0.2989 * k[0] + 0.5870 * k[1] + 0.1140 * k[2],\
                     0.5959 * k[0] - 0.2744 * k[1] - 0.3216 * k[2],\
                     0.2115 * k[0] - 0.5229 * k[1] + 0.3114 * k[2]] for k in r] for r in img])

def yiq_to_rgb(img):
  return rclip(np.array([[[k[0] + 0.9563 * k[1] + 0.6210 * k[2],\
                     k[0] - 0.2721 * k[1] - 0.6474 * k[2],\
                     k[0] - 1.1070 * k[1] + 1.7046 * k[2]]\
                     for k in r] for r in img]))

# Efeitos
def to_monochrome(img):
  return rclip(np.array([[[0.2126 * k[0] + 0.7152 * k[1] + 0.0722 * k[2] for f in range(3)] \
                  for k in r] for r in img]))

def to_monochrome_2D(img):
  return rclip(np.array([[0.2126 * k[0] + 0.7152 * k[1] + 0.0722 * k[2] \
                  for k in r] for r in img]))

def to_red(img):
  return np.array([[[k[0],0,0] for k in r] for r in img])

def to_green(img):
  return np.array([[[0,k[1],0] for k in r] for r in img])

def to_blue(img):
  return np.array([[[0,0,k[2]] for k in r] for r in img])

def mul_brightness(img,c):
  return rclip(np.array(\
    [[[k[0]*c ,k[1]*c,k[2]*c] for k in r] for r in img]))

def add_brightness(img,c):
  return rclip(np.array(\
    [[[k[0]+c ,k[1]+c,k[2]+c] for k in r] for r in img]))

def mul_brightness_yiq(img,c):
  return yiq_to_rgb(np.array(\
    [[[k[0]*c ,k[1],k[2]] for k in r] for r in rgb_to_yiq(img)]))

def add_brightness_yiq(img,c):
  return yiq_to_rgb(np.array(\
    [[[k[0]+c,k[1],k[2]] for k in r] for r in rgb_to_yiq(img)]))

def negative(img):
  return yiq_to_rgb(np.array([[[255 - k[0], k[1], k[2]] for k in r] for r in rgb_to_yiq(img)]))

def negative_rgb(img):
  return rclip(np.array([[[255 - k[0],255 - k[1],255 - k[2]] for k in r] for r in img]))


def limiar(img, t = 127):
  return np.array([[[(255 if (k[0] > t) else 0) for _ in range(3)] for k in r] for r in img])
