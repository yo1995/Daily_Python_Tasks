__author__ = 'cht'
'''
\begin{equation} \begin{cases} 
C_1 = C \cdot Alpha + 0 \cdot \left( 1 – Alpha \right) \\ 
C_2 = C \cdot Alpha + 1 \cdot \left( 1 – Alpha \right) 
\end{cases} \end{equation}

theory: see in readme

'''

import sys
import time
from PIL import Image, ImageEnhance
import matplotlib.pyplot as plt


def comp(c1, c2):
    c = round(255 * c1 / (255 + c1 - c2)) if 255 + c1 - c2 != 0 else 0
    alpha = 255 + c1 - c2 if 255 + c1 - c2 <= 255 else 255
    return c, alpha


def resize_image(d, b):
    width = min(d.size[0], b.size[0])
    height = min(d.size[1], b.size[1])
    # make a bad assumption here: landscape ratio comparison
    # might draw a rect to let usr judge if the crop is proper; otherwise reset and manually select

    crop_box = (0, 0, width, height)
    d = d.crop(crop_box)
    b = b.crop(crop_box)
    print(d.size[0], b.size[0], d.size[1], b.size[1])
    return d, b


if __name__ == '__main__':
    cwd = sys.path[0]
    darken_factor = float(input('please input the darken level factor(default 0.5): ') or 0.5)
    dark = input('please input the darker layer path: ') or cwd + '/dark.jpg'
    bright = input('please input the darker layer path: ') or cwd + '/bright.jpg'
    dark_image = Image.open(dark).convert('LA').split()[0]
    bright_image = Image.open(bright).convert('LA').split()[0]
    if dark_image.size != bright_image.size:
        dark_image, bright_image = resize_image(dark_image, bright_image)

    # plt.imshow(dark_image)
    # plt.ginput(1)
    # plt.clf()
    dark_image = ImageEnhance.Brightness(dark_image).enhance(darken_factor)
    # plt.imshow(dark_image)
    # plt.ginput(1)
    # plt.close()

    new_data = list(map(comp, dark_image.getdata(), bright_image.getdata()))  # vectorization!

    img = Image.new('LA', dark_image.size)
    img.putdata(new_data)

    img.save(cwd + '/output.png', 'PNG')
