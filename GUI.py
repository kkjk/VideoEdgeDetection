import matplotlib as plt
import cv2
import numpy as np

video = cv2.VideoCapture('C:\\Users\\keert\\Downloads\\bbb_sunflower_native_60fps_normal.mp4')  # Open Video

while (video.isOpened()):
    ret, frame = video.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    for n in ['frame', 'Edge']:
     cv2.namedWindow(n, cv2.WINDOW_NORMAL)
     cv2.resizeWindow(n, 600, 600)

## OpenCV canny edge detector for comparison
    edges = cv2.Canny(frame, 100, 200)

    display = np.hstack((gray, edges))

    cv2.imshow('frame', gray)
    cv2.imshow('Edge', edges)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
video.release()
cv2.destroyAllWindows()
