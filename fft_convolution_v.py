########################### Gaussian FFT ###################################


import numpy as np
from numpy import pi, exp, sqrt
import numpy.fft as fp



def gaussiankernel(imageshape,sigma=1.4, k_size=3):   ### k_size is the gaussian kernel size

    # sigma, k_size = 2, 3
    k_size = int(k_size/2)
    # print(k_size)
    gauss_1 = [exp(-x * x / (2 * sigma * sigma)) / sqrt(2 * pi * sigma * sigma) for x in range(-k_size, k_size + 1)]
    # print(gauss_1)
    gauss_kernel = np.outer(gauss_1, gauss_1)
    #print(gauss_kernel)
    kernelimage = np.zeros(imageshape)
    kernelimage[0:3, 0:3] = np.array(gauss_kernel,dtype=np.float32)
    return fp.fft2(kernelimage)


def fft_with_gaussian(image, kernel):
    # kernel = gaussiankernel(2, 3)
    # print(kernel)
    ## Embed kernel in image that is size of original image
    kernelimage = np.zeros(image.shape)   # image shape is 2250, 4000
    kernelimage[0:3, 0:3] = kernel

    #### 2d fft ################
    fimg = fp.fft2(image)
    fkernel = fp.fft2(kernelimage)
    #####  Set all zero values to minimum value
    # fkernel[abs(fkernel) < 1e-6] = 1e-6

    ### multiply fft
    f_req_img = fimg * fkernel * gaussiankernel(image.shape)

    req_img = fp.ifft2(f_req_img).real
    #print(np.max(req_img))
    req_img = req_img / 255.0
    return req_img

def fft(image, kernel):
        # kernel = gaussiankernel(2, 3)
        # print(kernel)
        ## Embed kernel in image that is size of original image
        kernelimage = np.zeros(image.shape)  # image shape is 2250, 4000
        kernelimage[0:3, 0:3] = kernel

        #### 2d fft ################
        fimg = fp.fft2(image)
        fkernel = fp.fft2(kernelimage)
        #####  Set all zero values to minimum value
        # fkernel[abs(fkernel) < 1e-6] = 1e-6

        ### multiply fft
        f_req_img = fimg * fkernel
        # print(np.max(fblurimg))

        req_img = fp.ifft2(f_req_img).real
        # print(np.max(blurimg))
        req_img = req_img / 255.0
        return req_img





