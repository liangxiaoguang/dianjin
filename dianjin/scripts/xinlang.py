from dj_app.models import xinlang
import requests
import time
import datetime
from lxml import etree
from html.parser import HTMLParser
import urllib.request

def get_html(url,Referer,encoding="utf-8",type='json'):
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

def add_index_to_mysql():
    # 定义一个存临时数据的数组
    temporary_list = []

    # 假设开始爬10W条
    count = 100000

    tips = 1  # 为不是重复

    for i in range(count):

        i += 1

        times = int(round(time.time() * 1000))

        url = "http://dj.sina.com.cn/ajax_list/get_recommend_article_list/1/{}?_={}".format(i, times)

        total_contend = get_html(url, "http://dj.sina.com.cn/information")

        #实际中存在有{'status': 'fail', 'game_list': []} ，新浪限制id最大只能为100，大于100，则需要对该情况进行判断

        if total_contend.get('status') =='fail':
            return '已爬取id完毕'

        # 拿到有需要数据的list
        data_list = total_contend.get('game_list').get('result').get('data').get('0')

        '''
        实际爬取过程中遇到一种情况
        如果脚本正在运行,然后又有新的新闻加入，导致查重，后面的数据不能被爬取到
        解决方案，做一个标示，要后面查找的10个都为重复则退出整个函数
        '''



        if tips != 1:
            return '已完成id接口爬虫，请等待详情页爬取'

        for data_ in data_list:


            # 发表时间
            ctime = data_.get("cTime")
            # id 唯一标识
            _id = data_.get('_id')
            # 标题
            title = data_.get('title')

            #temporary_list.append({'ctime': ctime, '_id': _id, 'title': title})

            #直接写数据库吧
            #首先判断该id是否存在如果存在则退出该 ---》***函数***
            one_entry = xinlang.objects.filter(c_id=_id)
            if one_entry.exists():
                #更新标示
                tips = 0
                continue
                #return '已完成id接口爬虫，请等待详情页爬取'

            #插入数据
            else:
                tips = 1
                xinlang.objects.create(c_id =_id, c_time = ctime,c_title = title)

            print(_id)

            #比较时间是否超过六个月
            # 转为时间数组，准备之后的比较
            timeArray = time.strptime(ctime, "%Y-%m-%d %H:%M:%S")

            timeStamp = int(time.mktime(timeArray))

            # 比较两者的时间戳,6个月的时间戳为86400*30*6 = 15552000,如果已经大于6个月了 则跳出循环
            # 只对数组的最后一个值进行比较
            if time.time() - timeStamp > 15552000:
                return '爬取时间已经超过六个月'


        time.sleep(5)


def get_content():

    #首先找到数据库中content为空的id
    obj_list = xinlang.objects.filter(content='')

    for obj in obj_list:

        print(obj.c_id)


        url = 'http://dj.sina.com.cn/article/{0}.shtml'.format(obj.c_id)
        html = get_html(url,'http://dj.sina.com.cn/information',type='text')


        selector = etree.HTML(html)

        rr_html = selector.xpath('//div[@id="artibody"]')[0]

        div_str = etree.tostring(rr_html,method='html')

        #解析html
        b = HTMLParser().unescape(div_str.decode())

        #获得这个里面的图片
        img_list = selector.xpath('//div[@class="img_wrapper"]//img//@src')


        for index,imgurl in enumerate(img_list):
            # urlretrieve() 方法直接将远程数据下载到本地。
            # 如果遇到也没得资源找不到的情况，try 然后跳过
            try:
                urllib.request.urlretrieve(imgurl,
                                           r"/root/img/xinlang/{}_{}.png".format(
                                               obj.c_id,index))


                #更换图片url
            except:
                continue
            b = b.replace(imgurl,'http://47.100.15.193/xinlang/{}_{}.png'.format(obj.c_id,index))

        obj.content = b
        obj.save()

    return '数据爬取完毕'

def run():
    print(add_index_to_mysql())
    print(get_content())