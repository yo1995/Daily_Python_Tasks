# -*- coding: utf-8 -*-

import os,sys,locale
from PIL import Image, ImageFont, ImageDraw
  
zihao = 100
img = Image.open('1.gif')
transparency = img.info['transparency']
text = raw_input(u'请输入需要转化的文字：\n'.encode('gb18030')).decode(sys.stdin.encoding or locale.getpreferredencoding(True))
im = Image.new("RGBA", (zihao*len(text) , zihao + 30), (0, 0, 0))
dr = ImageDraw.Draw(im)
font = ImageFont.truetype(os.path.join("fonts", "C:/Windows/Fonts/STZHONGS.TTF"), zihao)
dr.text((1, 1), text, font=font, fill="#111")


im.save(text + ".gif",transparency=transparency)
raw_input(u'表情已生成，任意键结束！')
