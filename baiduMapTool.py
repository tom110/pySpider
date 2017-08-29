from urllib import request
from bs4 import BeautifulSoup as bs
from urllib.parse import quote

print(quote("http://api.map.baidu.com/geocoder/v2/?address=明湖壹号&ak=0896a07cab9ee884b5747ed1a897d2d5",safe='/:?='))
req = request.Request(quote("http://api.map.baidu.com/geocoder/v2/?address=明湖壹号&ak=0896a07cab9ee884b5747ed1a897d2d5",safe='/:?=&'))
req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3080.5 Safari/537.36")
response = request.urlopen(req)
soup=bs(response.read().decode("utf-8"),"xml")
print(soup.prettify())
print(soup.find_all("lng")[0].string)
print(soup.find_all("lat")[0].string)