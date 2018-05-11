import urllib
import http.cookiejar
from bs4 import BeautifulSoup
from urllib import request


'''
发现有的网站存在请求返回空值的情况，简单研究了一下发现还是由于cookies构造出现了问题。
多数网站利用cookies来存储用户的访问信息，但像zol这样的网站没有返回cookie。
有几种思路：使用selenium模拟刷新；手动获取cookie后加载；想办法找到cookie。
采用了最后一种方法，想办法找个必含cookie的页面搞一波。
'''


def _getHeaders():
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
    # headers['Host'] = 'www.zol.com.cn'
    # headers['Connection'] = 'keep-alive'
    # headers['Cache-Control'] = 'max-age=0'
    headers['Accept-Language'] = 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7'
    # headers['Accept-Encoding']='gzip, deflate'
    headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
    headers['Referer'] = 'http://www.zol.com.cn/'
    return headers


if __name__ == '__main__':
    url0 = u'http://service.zol.com.cn/complain/'
    url1 = u'http://detail.zol.com.cn/index.php?c=SearchList&kword=%C8%FD%D0%C7'
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    urllib.request.install_opener(opener)
    req = urllib.request.Request(url0, headers=_getHeaders())
    req2 = urllib.request.Request(url1, headers=_getHeaders())
    opener.open(req)  # get cookie
    response = opener.open(req2)
    html = response.read()
    soup = BeautifulSoup(html, "html.parser", from_encoding="gbk")
    print(str(soup))

