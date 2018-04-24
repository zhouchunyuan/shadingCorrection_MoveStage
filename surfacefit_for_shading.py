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
        X.append(int(s1))
        Y.append(int(s2))
        Z.append(float(s3))
    return np.array(X),np.array(Y),np.array(Z)
def main():
    
    x,y,z = getdata()

    # Fit a 3rd order, 2d polynomial
    m = polyfit2d(x,y,z,4)

    # Evaluate it on a grid...
    nx, ny = 512, 512
    xx, yy = np.meshgrid(np.linspace(x.min(), x.max(), nx), 
                         np.linspace(y.min(), y.max(), ny))
    zz = polyval2d(xx, yy, m)

    # Plot
    plt.imshow(zz, extent=(x.min(), y.max(), x.max(), y.min()))
    #matplotlib.image.imsave('name.png', zz)
    plt.scatter(x, y, c=z)
    plt.show()

    im = Image.fromarray(zz)
    im.save('shadingCorrection.tif')# show how to save as tif with original data

def polyfit2d(x, y, z, order=3):
    ncols = (order + 1)**2
    G = np.zeros((x.size, ncols))
    ij = itertools.product(range(order+1), range(order+1))
    for k, (i,j) in enumerate(ij):
        G[:,k] = x**i * y**j
    m, _, _, _ = np.linalg.lstsq(G, z,rcond=None)
    return m

def polyval2d(x, y, m):
    order = int(np.sqrt(len(m))) - 1
    ij = itertools.product(range(order+1), range(order+1))
    z = np.zeros_like(x)
    for a, (i,j) in zip(m, ij):
        z += a * x**i * y**j
    return z

main()