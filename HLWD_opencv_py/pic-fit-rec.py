import cv2
import dlib
import sys
import multiprocessing
import time

detector = dlib.get_frontal_face_detector()  #使用默认的人类识别器模型
predictor = dlib.shape_predictor("./trained-set-data/shape_predictor_68_face_landmarks.dat")
cwd = sys.path[0]


def discern(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    dets = detector(gray, 1)
    for face in dets:
        left = face.left()
        top = face.top()
        right = face.right()
        bottom = face.bottom()
        shape = predictor(image, face)  # 寻找人脸的68个标定点
        # circle out all the points
        for pt in shape.parts():
            pt_pos = (pt.x, pt.y)
            cv2.circle(image, pt_pos, 2, (0, 255, 0), 1)
        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)


if __name__ == '__main__':
    t1 = time.time()
    img = cv2.imread('face.jpg')
    discern(img)
    print('time used: ' + str(time.time() - t1))
    cv2.imwrite(cwd + '/frame.jpg', img)
