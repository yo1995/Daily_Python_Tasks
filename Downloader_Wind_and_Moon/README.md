## 用法
根据fy.py文件内容使其运行起来，在链接部分输入存储《风月》专栏的文件名“links”即可开始下载。

## 设计思路与步骤
打开链接文件
循环读每一行，直接打开链接并截取链接日期部分
	创建文件夹：第00x期+title+日期
		循环下载图片：替换thumb部分内容，命名01-30等
	循环结束后：pyfpdf将图片合成一个PDF，文件名为第001期+title.pdf

## 参考内容
https://github.com/reingart/pyfpdf
urllib打开
https://www.cnblogs.com/Lucystonenix/p/5929931.html
http://www.runoob.com/python/python-func-filter.html
http://pyfpdf.readthedocs.io/en/latest/ReferenceManual/index.html
http://www.runoob.com/python/att-string-zfill.html
https://segmentfault.com/q/1010000004660365/a-1020000004847306
https://segmentfault.com/q/1010000008418332
等等

## 效果
![如图](https://raw.githubusercontent.com/yo1995/Daily_Python_Tasks/master/Wind_and_Moon/compilation.jpg)