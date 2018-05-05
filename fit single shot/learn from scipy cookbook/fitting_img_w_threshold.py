import itertools
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from scipy import optimize
from PIL import Image

def gaussian(height, center_x, center_y, width_x, width_y):
    """Returns a gaussian function with the given parameters"""
    width_x = float(width_x)
    width_y = float(width_y)
    return lambda x,y: height*np.exp(
                -(((center_x-x)/width_x)**2+((center_y-y)/width_y)**2)/2)

def moments(x,y,data):
    """Returns (height, x, y, width_x, width_y)
    x,y are 2D matrix of x and y coords
    the gaussian parameters of a 2D distribution by calculating its
    moments """
    total = data.sum()
    X, Y = x,y
    x0 = (X*data).sum()/total
    y0 = (Y*data).sum()/total
    width_x = X.max()-X.min()
    width_y = Y.max()-Y.min()
    height = data.max()
    return height, x0, y0, width_x, width_y

def fitgaussian(x,y,data):
    """Returns (height, x, y, width_x, width_y)
    the gaussian parameters of a 2D distribution found by a fit"""
    params = moments(x,y,data)
    errorfunction = lambda p: np.ravel(gaussian(*p)(x,y)-data)
    p, success = optimize.leastsq(errorfunction, params)
    return p

def getDataFromImage():
    background = 210
    pic = Image.open("sample.tif")
    pix = np.array(pic)
    pic_w = pix.shape[1]# x is the fast index
    pic_h = pix.shape[0]

    aspect = pic_h/pic_w

    y,x = np.array(np.where(pix>background))
    
    data = np.array(list(filter(lambda x:x>background,pix.flatten())))
    return x,y,data,(pic_w,pic_h)

   
Xin,Yin,data,size = getDataFromImage()
#plt.matshow(data, cmap=plt.cm.gist_earth_r)
params = fitgaussian(Xin,Yin,data)

Xout, Yout = np.mgrid[0:size[0], 0:size[1]]
fit = gaussian(*params)

plt.imshow(fit(Xout,Yout))

plt.show()
