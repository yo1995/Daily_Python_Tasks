import cv2 as cv
import sys

cwd = sys.path[0]
img = cv.imread(cwd + '/OpenCV.png')
cv.namedWindow('test')
cv.imshow('test', img)
cv.waitKey(0)
cv.destroyAllWindows()