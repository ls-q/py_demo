'''
对于crawl_mm_img修改
'''

import requests
import random
import re
import os
import time
#打开获取到的链接地址
def open_url(url):
    headers = {
        "Referer": url,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"}

    html = requests.get(url, headers=headers)

    return html
#获取当前页面中的图片的网址
def get_imgs(html):

    # img_lists = []

    pattern = re.compile(r'<li>.*?<a href="(http://www.mzitu.com/\d+)" target="_blank">', re.DOTALL)


    img_urls = re.findall(pattern, html.text)

    # for img_list in img_urls:
    #     img_lists.append(img_list)
    #

    return img_urls
    # return img_lists


def get_img_addrs(img_lists):

    # img_addrs = get_img_addrs(url)
    urls_child = []
    for img_list in img_lists:

        img_url = open_url(img_list)        # 获取当前图片的第一张
        pattern = re.compile(r'<div class="main-image">.*?<img src="(.*?.jpg)".*?</a>', re.DOTALL)
        url_child = re.findall(pattern, img_url.text)[0]
        urls_child.append(url_child)

    return urls_child

def save_imgs(folder,img_addrs):
    i = 1
    if i<=len(img_addrs):
        for img_addr in img_addrs:
            file_name = img_addr.split('/')[-1]

            with open(file_name,'wb') as f:
                resp = open_url(img_addr)
                f.write(resp.content)

                print('第{}张图片写入文件成功'.format(i))
                i+=1
                # time.sleep(4)

def crawl_mm_img(folder='pretty',img_type='',page_nums='5'):
    # folder = input('请输入文件夹的名称:')
    # print('妹子图网页中有如下类型：hot,best,zhuanti,xinggan,japan,taiwan,mm')
    # img_type = input('请输入图片的类型:')
    folder_path = 'C:/Users/Administrator/Desktop/{}'.format(folder)
    if not os.path.exists(folder):

        print('正在创建文件夹{}'.format(folder))
        os.mkdir(folder)
        os.chdir(folder)
        print('已切到{}文件夹'.format(folder))

    else:
        print('文件夹已经存在')
        os.chdir(folder)

    for page_num in range(1,page_nums+1):
        print('---------->>>>>正在下载第{}页：'.format(page_num))
        url ='http://www.mzitu.com/'+img_type+'/page/'+str(page_num)
        html = open_url(url)#获取当前页面
        img_lists = get_imgs(html)#获取当前页面中所有的图片列表
        img_addrs = get_img_addrs(img_lists)#获取每个图片的地址
        save_imgs(folder_path,img_addrs)#保持图片到本地
        # save_imgs(folder_path,img_lists)

if __name__ =='__main__':
    print('妹子图网页中有如下类型：hot,best,zhuanti,xinggan,japan,taiwan,mm')
    img_type = str(input('请输入图片的类型:'))
    page_nums = int(input("请输入有爬取的页面数:"))
    folder = input("请输入文件夹名称:")
    # for page_nums in range(pages_nums):
    crawl_mm_img(folder,img_type,page_nums)
