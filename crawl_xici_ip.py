import requests
from scrapy.selector import Selector
import MySQLdb
import datetime
import time

conn = MySQLdb.connect(host='localhost',user='root',password='root',db='article_spider',charset='utf8')
cursor = conn.cursor()

start = datetime.datetime.now()
print('开始的时间为:',start)#爬虫开始时的时间

def crawl_ips():

    #爬取西刺的免费IP代理
    # headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    for i in range(800):

        time.sleep(1)#防止爬取过快被封

        i +=1#从第一页开始

        url = 'http://www.xicidaili.com/nn/{0}'.format(i)#遍历所有的

        re = requests.get(url=url,headers=headers)#通过requests获取当前页面的response

        selector = Selector(text=re.text)

    #获取所有的ip列表

        all_trs = selector.css('#ip_list tr')

    #遍历获取到的ip列表
        ip_list = []
        for tr in all_trs[1:]:
            speed_tr = tr.css('.bar::attr(title)').extract()[0]
            if speed_tr:
                speed = float(speed_tr.split('秒')[0])#连接速度
            all_text =tr.css('td::text').extract()

            ip = all_text[0]#ip地址
            port = all_text[1]#端口号
            proxy_type = all_text[5]#协议类型
            ip_list.append((ip ,port ,speed ,proxy_type))

        for ip_info in ip_list:
            #将获取到的ip、Port、proxy_type插入到MySQL数据库
            cursor.execute("insert xici_ip(ip,port,speed,proxy_type) values('{0}','{1}',{2},'{3}')".format(ip_info[0],ip_info[1],ip_info[2],ip_info[3]))
            conn.commit()

    end =datetime.datetime.now()#爬虫结束的时间

    print('运行的时间为：',(end-start))#爬取所耗费的时间





crawl_ips()
