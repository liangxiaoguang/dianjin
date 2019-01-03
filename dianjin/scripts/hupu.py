from dj_app.models import duowan
import requests
import time
import datetime
from lxml import etree
from html.parser import HTMLParser
import urllib.request
import re


def get_html(url,Referer,type='json',encoding="utf-8"):
    try:
        headers = {
            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
            "Referer" : Referer
        }
        r = requests.get(url,headers=headers, timeout=30)
        r.raise_for_status()
        # 这里我们知道百度贴吧的编码是utf-8，所以手动设置的。爬去其他的页面时建议使用：
        #r.encoding = str(r.apparent_endconding).lower()
        r.encoding = encoding    #  'utf-8'   #gb2313 utf-8
        if type == 'json':
            return r.json()
        elif type == 'text':
            return r.text
    except Exception as e:
        print(e)
        return " ERROR "

def get_id():

    #数据较多 ，读取50页的数据

    #有五个分类

    #王者荣耀
    count = 100

    for i in range(count):

        i +=1

        url ='https://bbs.hupu.com/kog-postdate-{}'.format(i)

        html=get_html(url,'https://bbs.hupu.com/kog','text')



        # 解析html
        html = etree.HTML(html)

        list = html.xpath('//div[@class="titlelink box"]//a//@href')

        print(list)

        # for li in range(len(list)):
        #
        #     li += 1
        #
        #     url_id ='//ul[@class="for-list"]//li[{}]//div[1]//a//@href'.format(li)
        #
        #     #第一个标签url
        #     id = html.xpath(url_id)[0]
        #     print(id)
        #     #ctime =html.xpath('//ul[@class="for-list"]//li//div[2]//a[2]//text()')[0]


        return




def run():
    get_id()