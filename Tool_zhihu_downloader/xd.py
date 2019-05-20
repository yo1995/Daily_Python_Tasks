# -*- coding:utf-8 -*-

# 声明：知乎上某个答主写的爬虫脚本，代码没有整理，自己重新整理排版了，已经调试并通过
#      本人 Java 程序员，对 python 不熟，不过代码里面逻辑大概能看懂一些，这位答主的脚本是 python2 写的，
#      我自己是 python3 的环境，所以有些细微的改动，目的是为了兼容 python3 可以正常运行
#
#      原始脚本地址： https://www.zhihu.com/question/297715922/answer/676693318
#      如果觉得我冒犯了你的话，可以私信联系我，我删除。

import re
import requests
import os
import urllib.request
import ssl

from urllib.parse import urlsplit
from os.path import basename

# 全局禁用证书验证
ssl._create_default_https_context = ssl._create_unverified_context

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
    'Accept-Encoding': 'gzip, deflate'
}


def mkdir(path):
    if not os.path.exists(path):
        print('新建文件夹：', path)
        os.makedirs(path)
        return True
    else:
        print(u"图片存放于：", os.getcwd() + os.sep + path)
        return False


def download_pic2(img_lists, dir_name):
    print("一共有{num}张照片".format(num=len(img_lists)))

    # 标记下载进度
    index = 1

    for image_url in img_lists:
        file_name = dir_name + os.sep + basename(urlsplit(image_url)[2])

        # 已经下载的文件跳过
        if os.path.exists(file_name):
            print("文件{file_name}已存在。".format(file_name=file_name))
            index += 1
            continue

        auto_download(image_url, file_name)

        print("下载{pic_name}完成！({index}/{sum})".format(pic_name=file_name, index=index, sum=len(img_lists)))
        index += 1


def auto_download(url, file_name):
    # 递归下载，直到文件下载成功
    try:
        urllib.request.urlretrieve(url, file_name)
    except urllib.request.ContentTooShortError:
        print("文件下载不完整，重新下载。")
        auto_download(url, file_name)
    except urllib.request.URLError:
        print("网络连接出错，尝试重新下载。")
        auto_download(url, file_name)


def download_pic(img_lists, dir_name):
    print("一共有{num}张照片".format(num=len(img_lists)))
    for image_url in img_lists:
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            image = response.content
        else:
            continue

        file_name = dir_name + os.sep + basename(urlsplit(image_url)[2])

        try:
            with open(file_name, "wb") as picture:
                picture.write(image)
        except IOError:
            print("IO Error\n")
            continue
        finally:
            picture.close()

        print("下载{pic_name}完成！".format(pic_name=file_name))


def get_image_url(qid, headers):
    # 利用正则表达式把源代码中的图片地址过滤出来
    # reg = r'data-actualsrc="(.*?)">'
    tmp_url = "https://www.zhihu.com/node/QuestionAnswerListV2"
    size = 10
    image_urls = []

    session = requests.Session()

    while True:
        postdata = {'method': 'next',
                    'params': '{"url_token":' + str(qid) + ',"pagesize": "10",' + '"offset":' + str(size) + "}"}
        page = session.post(tmp_url, headers=headers, data=postdata)
        ret = eval(page.text)
        answers = ret['msg']
        print(u"答案数：%d" % (len(answers)))

        size += 10

        if not answers:
            print("图片 URL 获取完毕, 页数: ", (size - 10) / 10)
            return image_urls

        # reg = r'https://pic\d.zhimg.com/[a-fA-F0-9]{5,32}_\w+.jpg'
        imgreg = re.compile('data-original="(.*?)"', re.S)

        for answer in answers:
            tmp_list = []
            url_items = re.findall(imgreg, answer)

            for item in url_items:  # 这里去掉得到的图片 URL 中的转义字符'\\'
                image_url = item.replace("\\", "")
                tmp_list.append(image_url)

            # 清理掉头像和去重 获取 data-original 的内容
            tmp_list = list(set(tmp_list))  # 去重
            for item in tmp_list:
                if item.endswith('r.jpg'):
                    print(item)
                    image_urls.append(item)

        print('size: %d, num : %d' % (size, len(image_urls)))


if __name__ == '__main__':
    title = '拥有一副令人羡慕的好身材是怎样的体验？'
    question_id = 297715922

    # title = '身材好是一种怎样的体验？'
    # question_id = 26037846

    # title = '女孩子胸大是什么体验？'
    # question_id = 291678281

    # title = '女生什么样的腿是美腿？'
    # question_id = 310786985

    # title = '你的择偶标准是怎样的？'
    # question_id = 275359100

    # title = '什么样才叫好看的腿？'
    # question_id = 63727821

    # title = '身材对女生很重要吗？'
    # question_id = 307403214

    # title = '女生腿长是什么样的体验？'
    # question_id = 273711203

    # title = '女生腕线过裆是怎样一种体验？'
    # question_id = 315236887

    # title = '有着一双大长腿是什么感觉？'
    # question_id = 292901966

    # title = '拥有一双大长腿是怎样的体验？'
    # question_id = 285321190

    # title = '大胸女生如何穿衣搭配？'
    # question_id = 26297181

    # title = '胸大到底怎么穿衣服好看?'
    # question_id = 293482116

    zhihu_url = "https://www.zhihu.com/question/{qid}".format(qid=question_id)
    path = str(question_id) + '_' + title
    mkdir(path)  # 创建本地文件夹
    img_list = get_image_url(question_id, headers)  # 获取图片的地址列表
    download_pic2(img_list, path)  # 保存图片