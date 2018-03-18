# -*- coding: cp936 -*-
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import os,urllib2,time,re,sys,random

url = raw_input("please input the album url :")
# url = 'http://www.nfl.com/photos/0ap3000000633956'

def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/\:*?"<>|'
    new_title = re.sub(rstr, "", title)
    return new_title

def biaoti():
  soup = BeautifulSoup(content,"html.parser")
  title = str(soup.html.head.title)
  print title[24:-8]
  return title[24:-8]

def open1(url):
    browser = webdriver.Chrome()
    browser.get(url)
    browser.set_page_load_timeout(20)
    return browser.page_source

def page_loop():
  soup = BeautifulSoup(content,"html.parser")
  i = 0
  j = 0
  item = soup.find_all('div',class_='item')
  for qu in item:
    thumb = qu.find('div',class_='thumbnail')
    cl = qu.find('a',class_='content-link').find('span')
    for tupian in thumb:
      tutu = tupian.find('img')
      if not isinstance(tutu,int):
        link = tutu.get('src')
        try:
          flink = link.replace(u'_thumbnail_200_200',u'') #remove as original photo _pg_600
          content2 = urllib2.urlopen(flink).read()
        except Exception, e:
          try:
            flink = link.replace(u'thumbnail_200_200',u'gallery_600')
            content2 = urllib2.urlopen(flink).read()
          except Exception as e:
            try:
              flink = link.replace(u'_thumbnail_200_200', u'_pg_600')
              content2 = urllib.request.urlopen(flink).read()
            except Exception as e:
              print(u'Not Found or Bad Request !')
              continue
      else:
        j = 1

      i = int(i) + 1
	
    for sp in cl:
      ming1 = str(sp)
      print ming1
      with open(title+'/'+'('+str(i)+')'+validateTitle(ming1)+'.jpg','wb') as code:
        code.write(content2)
  # time.sleep(random.random())
  if (j):
    print u'Done!'
    sys.exit(0)
    



            
content = open1(url)
title = biaoti()
title=validateTitle(title)
path = os.getcwd()
new_path = os.path.join(path,title)
if not os.path.isdir(new_path):
  os.mkdir(new_path)

page_loop()
