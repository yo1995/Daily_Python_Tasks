import cv2
import dlib
import sys
import multiprocessing
import time

detector = dlib.get_frontal_face_detector()  #使用默认的人类识别器模型
predictor = dlib.shape_predictor("./trained-set-data/shape_predictor_68_face_landmarks.dat")
cwd = sys.path[0]


def discern(image, index, stacked):
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
    stacked[index] = image


if __name__ == '__main__':
    success = True
    cap = cv2.VideoCapture(cwd + '/face.mp4')
    fps = cap.get(cv2.CAP_PROP_FPS)
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    # fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(cwd + '/output.mp4', fourcc, fps, size)
    i = 0
    pool1 = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    pool1._taskqueue._maxsize = 4
    # stacked_frames = [None] * int(frames)
    sync_manager = multiprocessing.Manager()
    stacked_frames = sync_manager.list([None] * int(frames))
    t1 = time.time()
    while success:
        success, img = cap.read()
        pool1.apply_async(discern, args=(img, i, stacked_frames))
        # discern(img, writer)
        print(i)
        i = i + 1

    pool1.close()
    pool1.join()
    print('time used: ' + str(time.time() - t1))
    for i in range(len(stacked_frames)):
        # cv2.imwrite(cwd + '/out/frame' + str(i) + '.jpg', stacked_frames[i])
        writer.write(stacked_frames[i])

    cap.release()
    writer.release()
