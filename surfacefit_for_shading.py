import itertools
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

from PIL import Image

def getdata():
    file = open("shadingSample.txt","rb")
    buff = file.read().decode('utf-16')
    buff = buff.strip()#remove ending blank line
    lines = buff.split("\n")
    X=[]
    Y=[]
    Z=[]
    for line in lines:
        s1,s2,s3 = line.split(",")
        X.append(float(s1))
        Y.append(float(s2))
        Z.append(float(s3))
    return np.array(X),np.array(Y),np.array(Z)
def main():
    
    x,y,z = getdata()

    
    # Fit a 3rd order, 2d polynomial
    m = polyfit2d(x,y,z,4)

    # Evaluate it on a grid...
    # the range is fixed to 0...1
    nx, ny = 512, 512
    xx, yy = np.meshgrid(np.linspace(0, 1, nx), 
                         np.linspace(0, 1, ny))

    zz = polyval2d(xx, yy, m)

    # Plot
    plt.imshow(zz, extent=(0,1,1,0))
    #matplotlib.image.imsave('name.png', zz)
    plt.scatter(x, y, c=z)
    plt.show()

    saveImgs(zz,'shadingCorrection.tif')

    ######################### create a no-margin tif ################
    ######################### the edge is less affected #############
    xx0, yy0 = np.meshgrid(np.linspace(x.min(), x.max(), nx), 
                           np.linspace(y.min(), y.max(), ny))

    zz = polyval2d(xx0, yy0, m)

    saveImgs(zz,'shadingCorrection_soft.tif')

# change float array z to int
# sale the maximum to be 1000
# save it to tif image
def saveImgs(z,name):
    mx = np.amax(z)
    z1 = 1000/mx*z;
    im = Image.fromarray(z1.astype(np.uint16))
    im.save(name,'tiff')
    
def polyfit2d(x, y, z, order=3):
    ncols = (order + 1)**2
    G = np.zeros((x.size, ncols))
    ij = itertools.product(range(order+1), range(order+1))
    for k, (i,j) in enumerate(ij):
        G[:,k] = x**i * y**j
    m, _, _, _ = np.linalg.lstsq(G, z,rcond=-1)
    return m

def polyval2d(x, y, m):
    order = int(np.sqrt(len(m))) - 1
    ij = itertools.product(range(order+1), range(order+1))
    z = np.zeros_like(x)
    for a, (i,j) in zip(m, ij):
        z += a * x**i * y**j
    return z

main()
