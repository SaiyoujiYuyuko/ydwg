#-*- coding:utf-8 -*-
import json
import os
import csv
import codecs
import requests
from lxml import etree
from pip._vendor.distlib.compat import raw_input


class Spider:
    def __init__(self):
        self.ua_header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3278.0 Safari/537.36"}
        self.failitem=[]
        self.f=codecs.open('sht_torrent.csv','a+','utf-8')
        self.f_csv=csv.writer(self.f)
        if not os.path.isfile('sht_torrent.csv'):
            self.f_csv.writerow(['标题','磁力链接']) 

    def javSpider(self):
        choose = input('输入模式 0：仅上一次未成功的项 1：正常爬取模式\n')
        
        for item in self.failitemread():
            try:
                self.f_csv.writerow((item[0],self.gettorrent(item[1])))
            except:
                self.failitem.append(item)    
        
        choose = int(choose)
        if choose==0:
            return
        beginpage=input('输入起始页码：')
        endpage=input('请输入终止页码：')
        for page in range(int(beginpage),int(endpage)):
             try:
                 urllist = 'https://www.sehuatang.org/forum-103-'+str(page)+'.html'
                 self.loadPage(urllist)      
             except Exception as e:
                 print(e)
    #获取页面内容
    def loadPage(self, url):
        html=requests.get(url)
        selector = etree.HTML(html.text)
        javstar=selector.xpath('//*/table/*/tr/th/a[2]')
        torrentlist=[]
        for item in javstar:
            try:
                if '置顶' in item.text:
                    continue
                temp=(item.text,self.gettorrent('https://www.sehuatang.org/'+item.get('href')))
                print(temp)
                torrentlist.append(temp)
            except:
                self.failitem.append(item.text,'https://www.sehuatang.org/'+item.get('href'))
        self.f_csv.writerows(torrentlist)

    def gettorrent(self,url):
        html=requests.get(url)
        selector = etree.HTML(html.text)
        torrent = selector.xpath('//*/ol/li')
        for item in torrent:
            return item.text

    def failitemwrite(self):
        file = open('faileditem.txt', 'w+')
        file.write(json.dumps(self.failitem))
        file.close()

    def failitemread(self):
        file = codecs.open('faileditem.txt','w+','utf-8')
        lists=[]
        string = file.read()
        if len(string):
            print(string)
            lists=json.loads(string)
        print(lists)
        return lists

if __name__ == '__main__':
    mySpider = Spider()
    mySpider.javSpider()
    mySpider.failitemwrite()
