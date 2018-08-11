#! python3

import os
import re
import sys
import urllib.request
import time
import random
import multiprocessing


def download_pic(url1, url2, url3, new_path2, index):
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
                return False
    with open(new_path2, 'wb') as saved_pic:
        saved_pic.write(content)
        print('finish # ', index)
        return True


# main
if __name__ == '__main__':
    cwd = sys.path[0]
    filename = input("please input the links filename :")
    try:
        f = open(cwd + '/' + filename + '.txt', 'r', encoding='UTF-8')
    except:
        print('filename error')
        sys.exit(0)
    lines = f.readlines()
    count = len(lines)
    folder_name = input("please input the foldername :")
    initial = input("the initial letter of the model :")
    initial = '/' + initial.upper() + '.*.jpg'
    new_path = os.path.join(cwd, folder_name)
    if not os.path.isdir(new_path):
        os.mkdir(new_path)
    url = re.findall(r'src="(.+?\.jpg)"', lines[count - 2], re.I)
    print('the total # of files is: ' + str(len(url)))
    pool1 = multiprocessing.Pool(processes=4)
    pool1._taskqueue._maxsize = 16  # maximum number of processes added into taskqueue
    picture_download_timeout = 60

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
            print(i + 1, 'File already exist! Continue.')
            continue
        # time.sleep(random.random()) # to ensure that request is not too frequent
        # try:
        #     content = urllib.request.urlopen(url1).read()
        # except Exception as e:
        #     try:
        #         content = urllib.request.urlopen(url2).read()
        #     except Exception as e:
        #         try:
        #             content = urllib.request.urlopen(url3).read()
        #         except Exception as e:
        #             print(u'Not Found or Bad Request: ' + url0)
        #             continue
        #
        # with open(new_path2, 'wb') as saved_pic:
        #     saved_pic.write(content)
        print('current downloading', i + 1)
        pool1.apply_async(download_pic, args=(url1, url2, url3, new_path2, i + 1))
        # this part need to be polished.
        # assert (download_status_flag)  # False abort the main program

    pool1.close()
    pool1.join()
    print('==============================')
    print(u'All Done!')
    input('press any key to exit.')

    sys.exit(0)

