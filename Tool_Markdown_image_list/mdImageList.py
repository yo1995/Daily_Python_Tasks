import os
import sys

cwd = sys.path[0]
image_formats = {'.jpg', '.png', 'gif'}
images = []
others = []

prefix = input(u'请输入Git相对路径前缀(e.g. /images/2019rev/)：\n')

for filename in os.listdir(cwd):
    parts = os.path.splitext(filename)
    if parts[1] in image_formats:
        pathname = f'![{parts[0]}]({prefix}{filename})'
        images.append(pathname)
    else:
        pathname = f'[{parts[0]}]({prefix}{filename})'
        others.append(pathname)

print('-----images-----')
for image in images:
    print(image)
print('-----others-----')
for other in others:
    print(other)
os.system('pause')
