#### https://chengdu.anjuke.com/sale/p50/#filtersort
# 安居乐
#!/usr/bin/env python
#-*- coding:utf8 -*-
import requests
from lxml import etree
import time
import csv

def crawl(city, url):
    '''
    方法名称：spider
    功能：爬取目标网站，并以源码文本
    参数：url 目标网址
    :param url: 输入网址
    :return: 输出csv格式文本
    '''
    try:
        headers = {
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.1 Safari/605.1.15"
        }
        response = requests.get(url = url, headers = headers)
    except:
        print('failed to crawl the target site, please check if the url is correct or the collection is available!')

    res_xpath = etree.HTML(response.text)
    for num in range(1, 61):
        house_title = res_xpath.xpath('//li[%d]/div[2]/div[1]/a/text()' % num)[0].strip()
        house_mode = res_xpath.xpath('//li[%d]/div[2]/div[2]/span[1]/text()' % num)[0].strip()
        house_area = res_xpath.xpath('//li[%d]/div[2]/div[2]/span[2]/text()' % num)[0].strip()
        house_level = res_xpath.xpath('//li[%d]/div[2]/div[2]/span[3]/text()' % num)[0].strip()
        house_year = res_xpath.xpath('//li[%d]/div[2]/div[2]/span[4]/text()' % num)[0].strip()
        house_address = res_xpath.xpath('//li[%d]/div[2]/div[3]/span/text()' % num)[0].strip()
        house_totalprice = res_xpath.xpath('//li[%d]/div[3]/span[1]/strong/text()' % num)[0].strip() + '万'
        house_unitprice = res_xpath.xpath('//li[%d]/div[3]/span[2]/text()' % num)[0].strip()

        house_data = [house_title, house_mode, house_area, house_level, house_year, house_address, house_totalprice, house_unitprice]
        save_csv(city, house_data)

    print('finish download!')

def save_csv(city, house_data):
    '''
    方法名称：save_csv
    功能：将数据按行储存到csv文件中
    参数：house_data  获取到的房屋数据列表
    :param house_data: 获取到的房屋数据列表
    :return: 将房屋信息存储为csv格式
    '''
    try:
        with open(file = "%s_secondhouse_data.csv" % city, mode = 'a+', encoding = 'utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(house_data)
    except:
        print('write csv error!')

def get_all_urls(city, page_number):
    '''
    方法名称：get_all_urls
    功能：生成所有所有的url并存放到迭代器中
    参数：page_number    需要爬网页总数
    返回值：url          返回一个url的迭代
    :param page_number: 网址下页面编号
    :url: 网页地址（general) https://cd.fang.lianjia.com/loupan
    :return: 返回该网址下所有可能的页面的url
    '''
    if type(page_number) == type(1) and page_number > 0:
        for page in range(1, page_number + 1):
            url = 'https://%s.anjuke.com/sale/p%d/#filtersort' % (city, page)
            yield url
    else:
        print('page_number is incorrect')

# 首列写入
if __name__ == '__main__':
    # 新一线城市：cd--成都  hz--杭州  cq--重庆  wh--武汉  su--苏州  xa--西安  tj--天津
    # nj--南京  zz--郑州  cs--长沙  shen--沈阳  qd--青岛  nb--宁波  dg--东莞  wx--无锡
    # city = input('请输入一个城市拼音名：')

    city_set = ['chengdu', 'hangzhou', 'chongqing', 'wuhan', 'suzhou', 'xa', 'tianjin', 'nanjing', 'zhengzhou', 'cs', 'shenzhen', 'qd', 'nb', 'dg', 'wuxi']
    for i in range(len(city_set)):
        city = city_set[i]
        print(city)
        save_csv(city, ['house_title', 'house_mode', 'house_area', 'house_level', 'house_year', 'house_address', 'house_totalprice', 'house_unitprice'])
        all_urls = get_all_urls(city, 50)
        for url in all_urls:
            print(url)
            crawl(city, url)
            time.sleep(3)