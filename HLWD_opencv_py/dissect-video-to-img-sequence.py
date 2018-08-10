import cv2
import sys


cwd = sys.path[0]


if __name__ == '__main__':
    success = True
    cap = cv2.VideoCapture(cwd + '/face.avi')
    i = 0
    while success:
        success, img = cap.read()
        cv2.imwrite(cwd + '/out/frame' + str(i) + '.jpg', img)
        i = i + 1
