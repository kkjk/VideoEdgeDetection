img = cv2.imread('C:\\Users\\keert\\Pictures\\vlcsnap-2019-12-09-13h53m25s303.png')

# RGB to grey using PIL
# grey_img = Image.open(img).convert('LA')
# img.save('PIL_greyscale.png')

## RGB to Grey using OpenCV
# grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#
# for n in ['Grey Image', 'original']:
#     cv2.namedWindow(n, cv2.WINDOW_NORMAL)
#     cv2.resizeWindow(n, 600, 600)
#
# cv2.imshow('Grey Image', grey_img)
# cv2.imshow('original', img)
#
# cv2.waitKey(0)
# cv2.destroyAllWindows()