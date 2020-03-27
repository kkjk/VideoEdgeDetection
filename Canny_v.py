
########
from fft_convolution_v import fft_with_gaussian

import numpy as np



def sobel_edge_with_gaussian(image,edge_fil_x,edge_fil_y):
    '''
    Convolution with Sobel filter
    :param image: input image
    :param edge_fil_x: horizontal edge detecting filter
    :param edge_fil_y: vertical edge detecting filter
    :return: (derivatives) edge detected images
    '''

    sobel_x = fft_with_gaussian(image, edge_fil_x)

    sobel_y = fft_with_gaussian(image, edge_fil_y)

    return sobel_x, sobel_y

def gradient(sobel_x, sobel_y):
    '''
    Find the intensity gradients i.e, magnitude and angle of gradients
    :param sobel_x: derivative in x-direction
    :param sobel_y: derivative in y-direction
    :return: magnitude and angle of directional gradients
    '''


    grad_mag = np.sqrt(np.square(sobel_x) + np.square(sobel_y))
    grad_mag = grad_mag*255.0 / grad_mag.max()

    gradient_direction = np.arctan2(sobel_x, sobel_y)


    gradient_direction = np.rad2deg(gradient_direction)
    gradient_direction += 180

    return grad_mag, gradient_direction

def non_max_suppression_with_threshold_and_hystersis(grad_mag, grad_dir):
    '''
    Non maximum suppression to thin out the edges
    Double thresholding to remove noise
    Hysteresis to determine weak and actual edges
    :param grad_mag: magnitude of gradient
    :param grad_dir: angle of gradient
    :return: Image with thin edges
    '''
    M, N = grad_mag.shape
    I = np.zeros((M, N), dtype=np.int32)

    for i in range(1, M - 1):
        for j in range(1, N - 1):
            try:
                q = 255
                r = 255

                # angle 0
                if (0 <= grad_dir[i, j] < 22.5) or (157.5 <= grad_dir[i, j] <= 180):
                    q = grad_mag[i, j + 1]
                    r = grad_mag[i, j - 1]
                # angle 45
                elif (22.5 <= grad_dir[i, j] < 67.5):
                    q = grad_mag[i + 1, j - 1]
                    r = grad_mag[i - 1, j + 1]
                # angle 90
                elif (67.5 <= grad_dir[i, j] < 112.5):
                    q = grad_mag[i + 1, j]
                    r = grad_mag[i - 1, j]
                # angle 135
                elif (112.5 <= grad_dir[i, j] < 157.5):
                    q = grad_mag[i - 1, j - 1]
                    r = grad_mag[i + 1, j + 1]

                if (grad_mag[i, j] >= q) and (grad_mag[i, j] >= r):
                    I[i, j] = grad_mag[i, j]
                else:
                    I[i, j] = 0

                # double thresholding
                ##### low and high are respective thresholds
                high = 40
                low = 5
                if I[i,j] >= high :
                    I[i,j]=60
                if I[i,j]<high and I[i,j] > low:
                    I[i,j]=low
                # Hysterisis
                    if ((I[i + 1, j - 1] == high) or (I[i + 1, j] == high) or (I[i + 1, j + 1] == high)
                        or (I[i, j - 1] == high) or (I[i, j + 1] == high)
                        or (I[i - 1, j - 1] == high) or (I[i - 1, j] == high) or (I[i - 1, j + 1] == high)):
                        I[i, j] = high
                    else:
                        I[i, j] = 0
            except IndexError as e:
                pass

    return I


