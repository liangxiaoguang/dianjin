from dj_app.models import duowan
import requests
import time
import datetime
from lxml import etree
from html.parser import HTMLParser
import urllib.request
import re
from django.core.paginator import Paginator

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

    #写入10000条
    count = 100

    tips = 1  # 为不是重复

    for i in range(100):

        i += 1



        #组装后面的‘_2’数据,定义为index
        index = ''

        if i == 1:
            index = ''
        else:
            index = '_'+str(i)

        url = "http://news.duowan.com/tag/377717538395{}.html".format(index)

        sur_html = get_html(url,url,'text')

        #解析html
        html = etree.HTML(sur_html)

        type_list = html.xpath('//span[@class="from"]//text()')

        url_and_id_list = html.xpath('//a[@class="cover"]//@href')

        ctime_list =  html.xpath('//span[@class="date"]//text()')

        ctitle_list = html.xpath('//a[@class="cover"]//img//@alt')

        pic_list = html.xpath('//a[@class="cover"]//img//@src')

        #发现有分类为空的情况，导致数组没有26个值程序报错，对这种情况单独处理

        if len(type_list) != 26:
            #查看是哪个没有text，然后在数组中加上
            for index_,a in enumerate(url_and_id_list):
                check_url = '//a[@href="{}"]//..//div//div//span[@class="from"]//text()'.format(a)
                check_list = html.xpath(check_url)
                if len(check_list) == 0:
                    type_list.insert(index_, '其他')

        #判断标示
        if tips != 1:
            return '已完成id接口爬虫，请等待详情页爬取'

        #print(len(ctitle_list),ctitle_list)
        for index,_id in enumerate(url_and_id_list):
            print(_id)
            #写入数据库
            #1、首先判断数据库是否有该数据 有的话，就直接退出
            one_entry = duowan.objects.filter(c_id=_id)
            if one_entry.exists():
                tips = 0
                continue
                #return '已完成id接口爬虫，请等待详情页爬取'
            #2、写入数据库的逻辑
            else:
                tips = 1
                pic = pic_list[index]

                _id_index  = re.search('/(\d*).html', _id).group(1)
                # 下载图片和更换url
                try:
                    time.sleep(0.5)
                    urllib.request.urlretrieve(pic,
                                               r"/root/img/duowan/{}_{}.{}".format(
                                                   _id_index, 'homePic', pic.split(".")[-1]))
                    # 更换图片url
                except:
                    continue

                pic = pic.replace(pic, 'http://47.100.15.193/duowan/{}_{}.{}'.format(
                    _id, 'homePic', pic.split(".")[-1]))
                duowan.objects.create(c_id=_id, c_time=ctime_list[index], c_title=ctitle_list[index],style=type_list[index],pic = pic)

        time.sleep(5)

def get_content():

    #首先找到数据库中content为空的id
    obj_list = duowan.objects.filter(content='')

    for obj in obj_list:

        print(obj.c_id)

        html = get_html(obj.c_id,'http://news.duowan.com/',type='text')


        selector = etree.HTML(html)

        #发现有新的页面class =box-bd，如果这个页面出错的话 做个判断
        try:
            rr_html = selector.xpath('//div[@class="artical-bd"]')[0]
        except:
            obj.delete()
            continue

        div_str = etree.tostring(rr_html,method='html')

        #解析html
        b = HTMLParser().unescape(div_str.decode())

        #获得这个里面的图片
        img_list = selector.xpath('//div[@class="artical-bd"]//img//@src')

        print(len(img_list))
        for index,imgurl in enumerate(img_list):


            #有一张广告图，如果是广告图直接过滤，不需要下载
            if imgurl == 'http://img.dwstatic.com/pb/1803/385563596624/1521612376353.jpg':
                b = b.replace(imgurl, 'http://47.100.15.193/duowan/410354114273_5.jpg')
                continue

            id = re.search('/(\d*).html', obj.c_id).group(1)

            #查看该图片的后缀
            x = imgurl.split(".")
            # urlretrieve() 方法直接将远程数据下载到本地。
            # 如果遇到也没得资源找不到的情况，try 然后跳过
            try:
                time.sleep(0.5)
                #r"C:\Users\liangtian\Desktop\codedemo\reallywork\git\dianjin\img\duowan\{}_{}.{}"
                urllib.request.urlretrieve(imgurl,
                                           r"/root/img/duowan/{}_{}.{}".format(
                                               id,index,x[-1]))

                #更换图片url
            except:
                continue
            b = b.replace(imgurl,'http://47.100.15.193/duowan/{}_{}.{}'.format(id,index,x[-1]))

        obj.content = b
        obj.save()
    return '爬取完成'

def get_duowan(ps,pn):

    obj_list = duowan.objects.order_by('-c_time','now_time')

    p = Paginator(obj_list, ps)

    data = p.page(pn)

    datalist=[]

    for data_ in data.object_list:

        dict = {}

        dict['ctime'] = data_.c_time +" 00:00:00"

        dict['title'] = data_.c_title

        dict['content'] = data_.content

        # try:
        #     dict['content'] = dict['content'].replace(r".jpg/",".jpg")
        # except:
        #     pass
        #
        # try:
        #     dict['content'] = dict['content'].replace(r".png/",".png")
        # except:
        #     pass
        #
        # try:
        #     dict['content'] = dict['content'].replace(r".jpeg/",".jpeg")
        # except:
        #     pass
        #
        # try:
        #     dict['content'] = dict['content'].replace(r".gif/",".gif")
        # except:
        #     pass

        dict['id'] = data_.c_id

        dict['type'] = data_.style

        dict['pic'] = data_.pic

        datalist.append(dict)

    return datalist

def run():
    #print(get_duowan(10,1))
    print(get_id())
    print(get_content())


