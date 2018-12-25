import sys
import urllib.request

cwd = sys.path[0]
with open(cwd + '/links.txt', mode='r') as input_file:
    li = input_file.readlines()

i = 0
for line in li:
    i += 1
    content = urllib.request.urlopen(line).read()
    with open(cwd + '/' + str(i).zfill(3) + '.jpg', 'wb') as pic:
        pic.write(content)
    print(f'we are at pic {i}')
