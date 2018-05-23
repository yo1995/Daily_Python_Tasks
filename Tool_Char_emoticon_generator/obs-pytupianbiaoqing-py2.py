# -*- coding: utf-8 -*-

import os,sys,locale
import StringIO
from PIL import Image, ImageFont, ImageDraw
import pygame
  
pygame.init()
img = Image.open('3.gif')
transparency = img.info['transparency']

zihao = 100
text = raw_input(u'请输入需要转化的文字：\n'.encode('gb18030')).decode(sys.stdin.encoding or locale.getpreferredencoding(True))


im = Image.new("RGBA", (int(0.92*zihao*len(text)) , zihao + 30), (0, 0, 0))
font = pygame.font.Font(os.path.join("fonts", "C:/Windows/Fonts/STZHONGS.TTF"), zihao - 10)
  
# dr.text((10, 5), text, font=font, fill="#000000")
rtext = font.render(text, True, (0, 0, 0), (255, 255, 255))
sio = StringIO.StringIO()
pygame.image.save(rtext, sio)
sio.seek(0)

line = Image.open(sio)
im.paste(line, (1,1))
  
# im.show()
im.save(text + ".gif",transparency=transparency)
