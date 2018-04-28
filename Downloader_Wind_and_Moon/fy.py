import os
import re
import sys
import urllib.request
import requests
import time
import random
from PIL import Image
from bs4 import BeautifulSoup
from fpdf import FPDF


def generate_pdf(path, filename):
    ext_names = ['.JPG', '.jpg', '.jpeg']
    img = Image.open('./' + path + '/' + '(01).jpg')
    pdf = FPDF(unit='pt', format=img.size)
    for each_image in os.listdir('./' + path):
        for ext_name in ext_names:
            if each_image.endswith(ext_name):
                pdf.add_page()
                pdf.image('./' + path + '/' + each_image, 0, 0)
    pdf.output(filename + ".pdf", "F")


def validate_title(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/\:*?"<>|'
    new_title = re.sub(rstr, "", title)
    return new_title


def validate_period(period):
    period = re.sub("\D", "", period)
    return period


# main
if __name__ == '__main__':
    filename = input("please input the links filename :")
    f = open(filename + '.txt', 'r', encoding='UTF-8')
    lines = f.readlines()
    count = len(lines)
    print('the length of the links file is: ' + str(count))

    for i in range(0, count - 1):
        time.sleep(3 * random.random())
        url = re.search(r'http:.*.shtml', lines[i], re.I)
        try:
            url = url.group(0)
        except:
            print('Lines exceed the max amount. Finished.')
            sys.exit(0)
        print('==============================')
        date = re.search(r'/201.*?/', url)
        date = date.group(0)
        date = date[1: -1]
        print('Current link is: ' + url + ', ' + 'date is: ' + date)
        content = requests.get(url)
        content.encoding = 'UTF-8'
        content = content.text
        soup = BeautifulSoup(content, "html.parser")  # ,from_encoding="iso-8859-1"
        # title can be extract from links file.
        # title = soup.find('meta', attrs={"name": "description"})['content']
        title = re.search(r'titl.*.">', lines[i], re.I).group(0)
        title = title[7: -2]
        title = validate_title(title)
        # get the period of current page
        period = soup.find('div', class_='period')
        period = period.find('em').get_text()
        period = validate_period(period)
        folder_name = '第' + period.zfill(3) + '期_' + title + '_' + date
        print(folder_name)
        path = os.getcwd()
        new_path = os.path.join(path, folder_name)
        if os.path.isdir(new_path):
            print('Already exist! Continue.')
            continue
        os.mkdir(new_path)
        picList = soup.find('div', class_='tabViewList')
        thumbnail = picList.find_all('img')
        # print(len(thumbnail))
        ii = 0
        jj = 0
        for pic in thumbnail:
            ii = ii + 1
            pic_number = str(ii).zfill(2)  # to use 0X cardinal numbers
            if not isinstance(thumbnail, int):
                try:
                    pic_link = pic.get('src')
                    pic_link = pic_link.replace(u'http://d.ifengimg.com/w83_h56/', u'http://')
                    content = urllib.request.urlopen(pic_link).read()
                except Exception as e:
                    try:
                        pic_link = pic.get('_src')
                        pic_link = pic_link.replace(u'http://d.ifengimg.com/w83_h56/', u'http://')
                        content = urllib.request.urlopen(pic_link).read()
                    except Exception as e:
                        print(u'Not Found or Bad Request: ' + pic_link)
                        continue
            else:
                jj = 1 # finished

            with open(folder_name + '/' + '(' + pic_number + ')' + '.jpg', 'wb') as saved_pic:
                saved_pic.write(content)

        if jj or ii >= len(thumbnail):
            # might need to check the full length of the album
            print(u'Done!') # might not be visited? check later

        # to generate PDF
        generate_pdf(folder_name, folder_name)
    print('==============================')
    print(u'All Done!')
    sys.exit(0)

