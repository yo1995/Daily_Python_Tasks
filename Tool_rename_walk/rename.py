import os

path = ''

if not path:
    eixt(1)

for root, dirs, files in os.walk(path):
    for f in files:
        if f == 'readme.md':
            src = os.path.join(root, f)
            # print(src)
            dst = os.path.join(root, 'README.md')
            os.rename(src, dst) 
