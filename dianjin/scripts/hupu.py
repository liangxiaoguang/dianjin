import requests
from bs4 import BeautifulSoup
import pdb
from django.core.paginator import Paginator
import re
import gevent
import urllib.request
#from gevent import monkey; monkey.patch_all()
from gevent.queue import Queue
from dj_app.models import hupu
from lxml import etree
from html.parser import HTMLParser
import time
#返回一个url的text内容
def get_html(url,headers={},encoding="utf-8"):
    try:
        rs = requests.get(url, timeout=3,headers=headers)
        rs.encoding = encoding    #  'utf-8'   #gb2313 utf-8
        return rs.text

    except:
        return " ERROR "

#返回一个url被修饰后的结果，默认编码格式utf-8，headers为空
def get_content(url,headers={},encoding="utf-8"):
    #返回一个html格式的内容
    html = get_html(url,headers,encoding) 
    #用lxml解析html格式
    soup = BeautifulSoup(html, 'lxml')
    return soup,html


def get_bbs_urls(type, page_num=None):
    """ 
    type = "lol" or "kog" or "dota2"  "pubg" "ow" "hs" "game"
    """
    def _get_content(url, contents):
        content = get_content(url)
        return contents.put([ "https://bbs.hupu.com"+x.find('a',attrs={'href': re.compile('(\d)*.html$')}).get('href') for x in content.find('ul',attrs={'class':'for-list'}).find_all('li')])
    if page_num == None:
        page_num = 10
    urls = [f'https://bbs.hupu.com/{type}-postdate-' + str(x) for x in range(1,page_num+1)]
    gevent_contents = []
    contents = Queue()
    for url in urls:
        gevent_contents.append(gevent.spawn(_get_content, url, contents))
    gevent.joinall(gevent_contents)
    result = []
    while not contents.empty():
        result += contents.get()
    return result

def get_id():
    arr_list = ["lol", "kog", "dota2", "pubg", "ow", "hs", "game"]

    for all_url in arr_list:

        # 写入数据库
        type = ''
        if all_url == 'lol':
            type = '英雄联盟'
        elif all_url == 'kog':
            type = '王者荣耀'
        elif all_url == 'dota2':
            type = 'DOTA2'
        elif all_url == 'pubg':
            type = '绝地求生'
        elif all_url == 'ow':
            type = '守望先锋'
        elif all_url == 'hs':
            type = '炉石传说'
        elif all_url == 'game':
            type = '游戏'

        url_list = get_bbs_urls(all_url)

        for _id in url_list:

            # 判断重复的
            one_entry = hupu.objects.filter(c_id=_id)

            if one_entry.exists():
                continue
                # return '已完成id接口爬虫，请等待详情页爬取'
            # 2、写入数据库的逻辑
            else:
                print(_id)
                hupu.objects.create(c_id=_id, style=type)

        print('已完成' + all_url + '分类id爬取')

def inster_content():

    obj_list = hupu.objects.filter(content='')

    #print(len(obj_list))
    for obj in obj_list:

        result,html = get_content(obj.c_id)

        #

        try:
            print(obj.c_id)
            #pdb.set_trace()
            title = result.find('h1', attrs={'id':'j_data', 'data-maxpage':re.compile('(\d)*')}).text

        except AttributeError:

            try:
                #在数据库中删除该条数据
                hupu.objects.filter(c_id=obj.c_id).delete()
            except:
                continue

            continue
            # 时间

        ctime = result.find('span', attrs={'class':'stime'}).text

        # 正文
        #content = result.find('table', attrs={'class':'case', 'border':'0', 'cellspacing':'0'}).find('div',attrs={'class':'quote-content'})

        selector = etree.HTML(html)

        rr_html = selector.xpath('//div[@class="quote-content"]')[0]

        div_str = etree.tostring(rr_html, method='html')

        # 解析html
        b = HTMLParser().unescape(div_str.decode())

        img_list = selector.xpath('//div[@class="quote-content"]//p//img//@src')

        data_list = selector.xpath('//div[@class="quote-content"]//p//img//@data-original')

        #替换https://b1.hoopchina.com.cn/web/sns/bbs/images/placeholder.png

        # img_list1 = img_list
        # for index,i in  enumerate(img_list1):
        #     if i == 'https://b1.hoopchina.com.cn/web/sns/bbs/images/placeholder.png':
        #         url = '//div[@class="quote-content"]//p//img[{}]//@data-original'.format(index+1)
        #         print(url)
        #         img_list[index] = img_list = selector.xpath(url)[0]



        #第二种情况img_list没有取到数据
        if img_list == []:
            img_list = selector.xpath('//div[@class="quote-content"]//div//idiv//@src')

        #b = '<img src="https://i1.hoopchina.com.cn/blogfile/201901/07/BbsImg_53468974497719_1546864084_s_24009_o_w_250_h_375_12658.png?x-oss-process=image/resize,w_800/format,webp"'
        #print(re.findall('<img src="(.*)" ', b))
        l1 = []

        l1 = re.findall('(?<![video|script]) src="([^"]*)"', b)
        # 和下面的对应的
        # l1 = re.findall('<img src="([^"]*)" data-original="[^"]*"', b)
        l2=re.findall('(?<![video|script]) src="[^"]*" data-original="([^"]*)"', b)


        print(len(l1),len(l2),len(img_list))
        #测试用
        if len(img_list)>len(l1):
            print("_______________________________")
            return

        #print(len(img_list))
        if len(data_list) !=0:
            new_list = img_list[:-len(data_list)] + data_list
        else:
            new_list=img_list
        #print(len(new_list))



        id = re.search('/(\d*).html', obj.c_id).group(1)

        #替换图片
        for index_,imgurl in enumerate(img_list):
            try:
                time.sleep(0.5)
                #r"C:\Users\liangtian\Desktop\codedemo\reallywork\git\dianjin\img\duowan\{}_{}.{}"
                urllib.request.urlretrieve(new_list[index_],
                                           r"/root/img/hupu/{}_{}.jpg".format(
                                               id,index_))

                #更换图片url
            except:
                continue


            b = b.replace(imgurl,'http://47.100.15.193/hupu/{}_{}.jpg'.format(id,index_),2)
        #print(img_list)
        obj.content = b
        obj.c_title = title
        obj.c_time = ctime
        try:
            obj.save()
        except:
            continue


def get_hupu(ps,pn):

    obj_list = hupu.objects.exclude(content='').order_by('-c_time','now_time')

    p = Paginator(obj_list, ps)

    data = p.page(pn)

    datalist=[]

    for data_ in data.object_list:

        dict = {}

        dict['ctime'] = data_.c_time

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

    #get_id()
    inster_content()


    #result = get_content(all_urls[0])
    # # 标题
    # result.find('h1', attrs={'id':'j_data', 'data-maxpage':re.compile('(\d)*')}).text
    # # 时间
    # result.find('span', attrs={'class':'stime'}).text
    # # 正文
    # result.find('table', attrs={'class':'case', 'border':'0', 'cellspacing':'0'})
    # #pdb.set_trace()
    # print(result)