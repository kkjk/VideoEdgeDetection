
########
from fft_convolution_v import fft_with_gaussian

import numpy as np



def sobel_edge_with_gaussian(image,edge_fil_x,edge_fil_y):

    sobel_x = fft_with_gaussian(image, edge_fil_x)

    sobel_y = fft_with_gaussian(image, edge_fil_y)

    return sobel_x, sobel_y

def gradient(sobel_x, sobel_y):

    grad_mag = np.sqrt(np.square(sobel_x) + np.square(sobel_y))
    grad_mag = grad_mag*255.0 / grad_mag.max()

    gradient_direction = np.arctan2(sobel_x, sobel_y)


    gradient_direction = np.rad2deg(gradient_direction)
    gradient_direction += 180

    return grad_mag, gradient_direction

def non_max_suppression_with_threshold_and_hystersis(grad_mag, grad_dir):
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
                ###### low and high are respective thresholds
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


'''
cap = cv2.VideoCapture('sample.mp4')
print(cap.get(cv2.CAP_PROP_POS_MSEC))
print(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(cap.get(cv2.CAP_PROP_FPS))
# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'FMP4')
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (400,226))
edge_fil_x = np.asarray([[-1, 0, 1],
                         [-2, 0, 2],
                         [-1, 0, 1]])
edge_fil_y = np.flip(edge_fil_x.T, axis=0)

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        g_x, g_y = sobel_edge_with_gaussian(grayFrame)
        g, d = gradient(g_x, g_y)
        V = non_max_suppression_with_threshold_and_hystersis(g, d)
        V = np.array(V, dtype=np.float32)

        # write the flipped frame
        currentframe=+1
        out.write(cv2.cvtColor(V, cv2.COLOR_GRAY2BGR))

        cv2.imshow('frame',V)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()'''