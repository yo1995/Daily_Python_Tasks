#! python3

import os
import re
import sys
import urllib.request
import time
import random

# main
if __name__ == '__main__':
    filename = input("please input the links filename :")
    try:
        f = open(filename + '.txt', 'r', encoding='UTF-8')
    except:
        print('filename error')
        sys.exit(0)
    lines = f.readlines()
    count = len(lines)
    folder_name = input("please input the foldername :")
    initial = input("the initial letter of the model :")
    initial = '/' + initial.upper() + '.*.jpg'
    path = os.getcwd()
    new_path = os.path.join(path, folder_name)
    if not os.path.isdir(new_path):
        os.mkdir(new_path)
    url = re.findall(r'src="(.+?\.jpg)"', lines[count - 2], re.I)
    print('the total # of files is: ' + str(len(url)))
    for i in range(0, len(url)):
        try:
            url0 = url[i]
        except:
            print('url list error')
            sys.exit(0)
        # print('==============================')
        url0 = url0.replace(u'small-', u'')
        url1 = url0.replace(u'/ssd/small/', u'/uploads3/pixsense/big/')
        url2 = url0.replace(u'/ssd/small/', u'/uploads4/pixsense/big/')
        # special for GFW
        url3 = url0.replace(u'http://www.pixsense.net/', u'http://www.fortstore.net/')
        url3 = url3.replace(u'/default/upload/', u'/latest/uploads1/pixsense/big/')
        url3 = url3.replace(u'/latest/uploads/', u'/latest/uploads1/pixsense/big/')
        url3 = url3.replace(u'-1-', u'-0-')
        picname = re.search(initial, url0, re.I)
        if picname is None:
            picname = '/' + str(i + 1).zfill(3) + '.jpg'
        else:
            picname = picname.group(0)
        new_path2 = new_path + picname
        if os.path.isfile(new_path2):
            print('File already exist! Continue.')
            continue
        # time.sleep(random.random()) # to ensure that request is not too frequent
        try:
            content = urllib.request.urlopen(url1).read()
        except Exception as e:
            try:
                content = urllib.request.urlopen(url2).read()
            except Exception as e:
                try:
                    content = urllib.request.urlopen(url3).read()
                except Exception as e:
                    print(u'Not Found or Bad Request: ' + url0)
                    continue

        with open(new_path2, 'wb') as saved_pic:
            saved_pic.write(content)

    print('==============================')
    print(u'All Done!')
    sys.exit(0)

