import time
from PIL import Image
import sys
import psutil
import os


def _color_diff(rgb1, rgb2):
    """
    Uses 1-norm distance to calculate difference between two rgb values.
    """
    return abs(rgb1[0]-rgb2[0]) + abs(rgb1[1]-rgb2[1]) + abs(rgb1[2]-rgb2[2])


def flood_fill_full(image, xy, value, thresh=0):
    pixel = image.load()
    x, y = xy
    try:
        background = pixel[x, y]
        if _color_diff(value, background) <= thresh:
            return  # seed point already has fill color
        pixel[x, y] = value
    except (ValueError, IndexError):
        return  # seed point outside image
    edge = {(x, y)}
    full_edge = set()
    i = 0
    while edge:
        new_edge = set()
        for (x, y) in edge:  # 4 adjacent method
            for (s, t) in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):

                if (s,t) in full_edge:
                    continue
                i = i + 1
                try:
                    p = pixel[s, t]
                except IndexError:
                    pass
                else:
                    if _color_diff(p, background) <= thresh:
                        pixel[s, t] = value
                        new_edge.add((s, t))
                        full_edge.add((s, t))
        edge = new_edge
    print('total iteration: ' + str(i))


if __name__ == '__main__':
    img_path = sys.argv[1]
    img0 = Image.open(img_path)
    t1 = time.time()
    flood_fill_full(img0, (1, 1), (0, 255, 0), 0)
    print('time used: ' + str(time.time() - t1))
    print('mem used: ' + str(psutil.Process(os.getpid()).memory_info().rss))
