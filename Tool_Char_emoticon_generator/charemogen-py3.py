# -*- coding: utf-8 -*-

import os
import sys
import re
import string
from PIL import Image, ImageFont, ImageDraw


def validate_title(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/\:*?"<>|'
    new_title = re.sub(rstr, "", title)
    return new_title


if __name__ == '__main__':
    zihao = 100
    char_len = 0
    current_dir = sys.path[0]
    img = Image.open(current_dir + '/1.gif')
    transparency = img.info['transparency']
    text = input(u'请输入需要转化的文字：\n')
    for char in text:
        if char in string.ascii_letters:
            char_len = char_len + 1
    im = Image.new("RGBA", (zihao*int(len(text)-0.5*char_len), zihao + 30), (0, 0, 0))
    dr = ImageDraw.Draw(im)
    font = ImageFont.truetype(os.path.join("fonts", "C:/Windows/Fonts/STZHONGS.TTF"), zihao)
    dr.text((1, 1), text, font=font, fill="#111")

    im.save(current_dir + '/' + validate_title(text) + ".gif", transparency=transparency)
    input(u'表情已生成，任意键结束！')
