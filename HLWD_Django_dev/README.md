![logo](djangopony.png)

## 初始化

python3 -m venv Django
source Django/bin/activate
pip3 install Django

deactivate

## 启动服务

django-admin startproject mysite

python manage.py runserver 0.0.0.0:8000  # 对外网打开访问

Invalid HTTP_HOST header: 'IP：port'. You may need to add u'IP' to ALLOWED_HOSTS.

在settings.py 中修改
ALLOWED_HOSTS = ['IP']

## favicon.ico
from django.contrib.staticfiles.views import serve
path('favicon.ico', serve, {'path': '/favicon.ico'}),

## Directory optimization

http://www.loonapp.com/blog/11/

https://blog.csdn.net/qq_16260961/article/details/72972839

 mv polls apps/polls


## Requirements
pip freeze > requirements.txt

## 数据库操作
不用SQL语句，调用API就可以查表。

每次更新表结构后需要migrate，具体为

- Change your models (in models.py).
- Run python manage.py makemigrations to create migrations for those changes
- Run python manage.py migrate to apply those changes to the database.

