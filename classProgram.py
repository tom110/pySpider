from urllib import request
from bs4 import BeautifulSoup as bs
import re
import pymysql.cursors
from urllib.parse import quote
import time


class PyReptile:
    # 初始化方法，定义一些变量
    def __init__(self, userAgent):
        self.userAgent = userAgent
        self.usedUrl = []

    def start(self, url, host,city):
        # 处理入口页面
        soup = self.getSoup(url, host)
        urls = self.getUrl(soup)
        # self.showInfo(soup)
        self.saveMysql(soup)
        self.usedUrl.append(url)

        # 处理子页面
        for url in urls:
            if url not in self.usedUrl:
                self.start(url, host)

    def showInfo(self, soup,city):
        for div in soup.find_all("div", {"class", "item-mod"}):
            # print(div.select("a.items-name").string+"<---->"+div.select("span").string)
            if len(div.select("a.items-name")) != 0:
                print(
                    div.select("a.items-name")[0].string + "<----->" + div.select("i.status-icon")[0].string + "<----->"
                    + div.select("p > span")[0].string + "<--->" + div.select("p.address")[0].find("a").string)

    def saveMysql(self, soup,city):
        for div in soup.find_all("div", {"class", "item-mod"}):
            if len(div.select("a.items-name")) != 0:
                connection = pymysql.connect(host='localhost',
                                             user='root',
                                             password='root',
                                             db='pdb',
                                             charset='utf8')
                try:
                    with connection.cursor() as cursor:
                        sql = "insert into `pytable`(`name`,`state`,`price`,`address`) value(%s,%s,%s,%s)"

                        cursor.execute(sql, (
                            div.select("a.items-name")[0].string, div.select("i.status-icon")[0].string,
                            div.select("p > span")[0].string, div.select("p.address")[0].find("a").string))
                        connection.commit()
                finally:
                    connection.close()

    def getUrl(self, soup):
        listUrls = soup.find_all("div", {"class", "pagination"})[0].select("a")
        urls = []
        for url in listUrls:
            # print(url.string + "<--->" + url["href"])
            urls.append(url["href"])
        return urls

    def getSoup(self, url, host):
        req = request.Request(url)
        req.add_header("Host", host)
        req.add_header("User-Agent", self.userAgent)
        response = request.urlopen(req)
        # print(response.read().decode("utf-8"))
        soup = bs(response.read().decode("utf-8"), "html.parser")
        return soup


# 槐荫爬虫(废弃)
# class HuaiYinAnJuKeSpider(PyReptile):
#     def __init__(self,userAgent):
#         super(HuaiYinAnJuKeSpider, self).__init__(userAgent)
#
# pyReptileHuaiyin = HuaiYinAnJuKeSpider(
#     "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3080.5 Safari/537.36")
#
# pyReptileHuaiyin.start("http://jn.fang.anjuke.com/loupan/huaiyin/", "jn.fang.anjuke.com")

# ****槐荫爬虫

# 济南全部爬虫
class AllAnJuKeSpider(PyReptile):
    def __init__(self, userAgent):
        super(AllAnJuKeSpider, self).__init__(userAgent)

    def start(self, url, host, city):
        # 处理入口页面
        soup = self.getSoup(url, host)
        urls = self.getUrl(soup)
        self.showInfo(soup,city)
        # self.saveMysql(soup, city)
        self.usedUrl.append(url)

        # 处理子页面
        for url in urls:
            if url not in self.usedUrl:
                self.start(url, host,city)

    def showInfo(self, soup, city):
        for div in soup.find_all("div", {"class", "item-mod"}):
            # print(div.select("a.items-name").string+"<---->"+div.select("span").string)
            if len(div.select("a.items-name")) != 0:
                if len(div.select("p[class$='price']")) != 0:
                    name = div.select("a.items-name")[0].string
                    address = div.select("p.address")[0].find("a").string
                    lng, lat = self.getLngLat(name, address, city)
                    print(
                        name + "<----->" + div.select("i.status-icon")[
                            0].string + "<----->"
                        + div.select("p[class$='price']")[0].find(
                            "span").string + "<--->" + address + "<----->" + lng + "<----->" + lat + "<--->" + time.strftime(
                            '%Y-%m-%d', time.localtime(time.time())))

    def saveMysql(self, soup, city):
        for div in soup.find_all("div", {"class", "item-mod"}):
            if len(div.select("a.items-name")) != 0:
                if len(div.select("p[class$='price']")) != 0:
                    connection = pymysql.connect(host='192.168.50.251',
                                                 user='root',
                                                 password='root',
                                                 db='pdb',
                                                 charset='utf8')
                    try:
                        with connection.cursor() as cursor:
                            sql = "insert into `pytable`(`name`,`state`,`price`,`address`,`lng`,`lat`,`gettime`) value(%s,%s,%s,%s,%s,%s,%s)"
                            name = div.select("a.items-name")[0].string
                            address = div.select("p.address")[0].find("a").string
                            lng, lat = self.getLngLat(name, address, city)
                            gettime = time.strftime('%Y-%m-%d', time.localtime(time.time()))

                            cursor.execute(sql, (
                                name, div.select("i.status-icon")[0].string,
                                div.select("p[class$='price']")[0].find("span").string, address, lng, lat, gettime))
                            connection.commit()
                    finally:
                        connection.close()

    def getLngLat(self, name, address, city):
        req = request.Request(
            quote(
                "http://api.map.baidu.com/geocoder/v2/?address=" + address + "&ak=0896a07cab9ee884b5747ed1a897d2d5&city=" + city,
                safe='/:?=&'))
        req.add_header("User-Agent",
                       "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3080.5 Safari/537.36")
        req.add_header("host", "api.map.baidu.com")
        response = request.urlopen(req)
        soup = bs(response.read().decode("utf-8"), "xml")
        lngList = soup.find_all("lng")
        latList = soup.find_all("lat")

        if (len(lngList) != 0 and len(latList) != 0):
            return soup.find_all("lng")[0].string, soup.find_all("lat")[0].string
        else:
            req = request.Request(
                quote(
                    "http://api.map.baidu.com/geocoder/v2/?address=" + name + "&ak=0896a07cab9ee884b5747ed1a897d2d5&city=济南市",
                    safe='/:?=&'))
            req.add_header("User-Agent",
                           "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3080.5 Safari/537.36")
            req.add_header("host", "api.map.baidu.com")
            response = request.urlopen(req)
            soup = bs(response.read().decode("utf-8"), "xml")
            lngList = soup.find_all("lng")
            latList = soup.find_all("lat")

            if (len(lngList) != 0 and len(latList) != 0):
                return soup.find_all("lng")[0].string, soup.find_all("lat")[0].string
            else:
                return "", ""


pyReptileAll = AllAnJuKeSpider(
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3080.5 Safari/537.36")

pyReptileAll.start("http://jn.fang.anjuke.com/loupan/all/", "jn.fang.anjuke.com","济南市")

#***济南全部爬虫

# # 青岛全部爬虫
# pyReptileAll = AllAnJuKeSpider(
#     "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3080.5 Safari/537.36")
#
# pyReptileAll.start("http://qd.fang.anjuke.com/loupan/all/", "qd.fang.anjuke.com", "青岛市")
# # ***青岛全部爬虫
