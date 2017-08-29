from urllib import request
from bs4 import BeautifulSoup as bs
import re
import pymysql.cursors



req = request.Request("http://jn.fang.anjuke.com/loupan/huaiyin/")
req.add_header("Host", "jn.fang.anjuke.com")
req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3080.5 Safari/537.36")
response = request.urlopen(req)
# print(response.read().decode("utf-8"))

soup=bs(response.read().decode("utf-8"),"html.parser")
# print(soup.prettify())
# print(soup.title.string)
# listUrls=soup.find_all("a",href=re.compile(r"^http://jn.fang.anjuke.com/loupan/huaiyin/p"))
# for url in listUrls:
#     print(url.string+"<--->"+url["href"])
for div in soup.find_all("div",{"class", "item-mod"}):
    # print(div.select("a.items-name").string+"<---->"+div.select("span").string)
    if len(div.select("a.items-name")) != 0:
        print(div.select("a.items-name")[0].string+"<----->"+div.select("i.status-icon")[0].string+"<----->"
              +div.select("p > span")[0].string+"<--->"+div.select("p.address")[0].find("a").string)

        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='root',
                                     db='pdb',
                                     charset='utf8')
        try:
            with connection.cursor() as cursor:
                sql = "insert into `pytable`(`name`,`state`,`price`,`address`) value(%s,%s,%s,%s)"

                cursor.execute(sql, (div.select("a.items-name")[0].string, div.select("i.status-icon")[0].string,div.select("p > span")[0].string,div.select("p.address")[0].find("a").string))
                connection.commit()
        finally:
            connection.close()


