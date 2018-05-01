#https://stackoverflow.com/questions/27539933/2d-gaussian-fit-for-intensities-at-certain-coordinates-in-python
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt

def main():
##    x0, y0 = 0.3, 0.7
##    amp, a, b, c = 1, 2, 3, 4
##    true_params = [amp, x0, y0, a, b, c]
##    xy, zobs = generate_example_data(10, true_params)
##    x,y = xy

    pic = Image.open("sample.tif")
    #pic.show()
    pix = np.array(pic)
    #print(pix[20,20],pix[110,20])
    pic_w = pix.shape[1]# x is the fast index
    pic_h = pix.shape[0]

    aspect = pic_h/pic_w

    xi = np.array(np.where(pix>210))[1]
    yi = np.array(np.where(pix>210))[0]
    x = xi/pic_w
    y = yi/pic_h*aspect
    xy = np.array([x,y])

    #print(x)
    threshold = []
    mx = np.max(pix)
    for i in range(len(xi)):
        threshold.append(pix[yi[i],xi[i]])
        
    zobs = np.array(threshold)-100
    
  
    #i = zobs.argmax()
    #guess = [1, x[i], y[i], 1, 1, 1]
    amp0 = zobs.max()
    guess = [amp0, 0.5, 0.5, 1]
    pred_params, uncert_cov = opt.curve_fit(gauss2d, xy, zobs, p0=guess)

    zpred = gauss2d(xy, *pred_params)
    #print ('True parameters: ', true_params)
    print ('Predicted params:', pred_params)
    print ('Residual, RMS(obs - pred):', np.sqrt(np.mean((zobs - zpred)**2)))

    plot(xy, zobs, pred_params)
    plt.show()
    
# simplified 2D gaussian
# exp(-[(x-x0)^2+(y-y0)^2]/c^2)
def gauss2d(xy, amp, x0, y0, c):
    x, y = xy
    inner = (x - x0)**2
    inner += (y - y0)**2
    return amp * np.exp(-inner/(c*c))

def generate_example_data(num, params):
    np.random.seed(1977) # For consistency
    xy = np.random.random((2, num))

    zobs = gauss2d(xy, *params)
    return xy, zobs

def plot(xy, zobs, pred_params):
    x, y = xy
    yi, xi = np.mgrid[:1:512j, :1:512j]
    xyi = np.vstack([xi.ravel(), yi.ravel()])##############<<<---------

    zpred = gauss2d(xyi, *pred_params)
    zpred.shape = xi.shape
    
    im_ = Image.fromarray(zpred)
    im_.save('fitting.tif','tiff')
    
    fig, ax = plt.subplots()
    ax.scatter(x,y, c=zobs, s=1, vmin=zpred.min(), vmax=zpred.max())
    im = ax.imshow(zpred, extent=[xi.min(), xi.max(), yi.max(), yi.min()],
                   aspect='auto')
    fig.colorbar(im)
    ax.invert_yaxis()
    return fig

main()
#######################################3




