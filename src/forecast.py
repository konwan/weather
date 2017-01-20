#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import queue
import datetime
import threading
import random
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import os, sys
from outputdata import OutputData

class ForecastWeather(OutputData):
    def __init__(self, *args, **kwargs):
        super(ForecastWeather, self).__init__(*args, **kwargs)
        self.cities = []
        self.datatype = "forecast"
        self.dir_path = os.path.dirname(os.path.realpath('__file__'))
        # self.city = city
        # self.raw_url = url
        # self.url = Request(url)
        # self.datadir = '{}/{}/{}'.format(self.dir_path, self.datatype, self.city)
        # self.raw = None
        # self.res = None
        # self.alldays = []
        self.today = datetime.datetime.now().strftime("%Y%m%d")
        self.updatetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # self.start()

    # def cusHeader(self, raw_url=None):
    #     if raw_url is not None :
    #         url = Request(raw_url)
    #         url.add_header('User-Agent', 'Mozilla/5.0 Chrome/55.0.2883.95 Safari/{}.36'.format(random.randint(0, 30)))
    #         url.add_header('Referer', raw_url)
    #         try:
    #             # time.sleep(random.randint(0, 2))
    #             raw = urlopen(url)
    #             print(raw.status)
    #             # print(raw.getheaders())
    #             # self.res = BeautifulSoup(self.raw.read(), "lxml", from_encoding="GBK")
    #         except Exception as e:
    #             print('[open page fail] {} => {}'.format(raw_url, str(e)))
    #             sys.exit()

    # def getdata(self):
    #     for i in range(3):
    #         try:
    #             tmp = self.res.select('#today')[i].text.strip().split('\n')
    #             tmp_date = datetime.date.today() + datetime.timedelta(days=i)
    #
    #             date = tmp_date.strftime("%Y-%m-%d") # tmp[2][0:2]+tmp[2][3:5]
    #             htemp = tmp[5].replace('℃','').split('~')[0]
    #             ltemp = tmp[5].replace('℃','').split('~')[1]
    #             status = tmp[7]
    #             winddir = tmp[8].split(' ')[0]
    #             windpower = tmp[8].split(' ')[1]
    #         except Exception as e:
    #             print('[3Error] {} => {}'.format(self.raw_url, str(e)))
    #             time.sleep(10)
    #             sys.exit()
    #         self.alldays.append([self.city, date, htemp, ltemp, status, winddir, windpower, self.updatetime])
    #
    #     other_4days = self.res.select('#detail')[0]
    #
    #     for i in range(1,5):
    #         try :
    #             j = self.res.select('#detail')[0].select('div:nth-of-type({})'.format(i))[0].text.strip().split('\n')
    #             tmp_date = datetime.date.today() + datetime.timedelta(days=(i+2))
    #             date = tmp_date.strftime("%Y-%m-%d") # j[0][0:2]+j[0][3:5]
    #             htemp = j[5].replace('℃','').split('~')[0]  if len(j) == 7 else ''
    #             ltemp = j[5].replace('℃','').split('~')[1]  if len(j) == 7 else ''
    #             status = j[3].split('：')[1]  if len(j) == 7 else ''
    #             winddir = j[6].split(' ')[0]  if len(j) == 7 else ''
    #             windpower = j[6].split(' ')[1] if len(j) == 7 else ''
    #         except Exception as e:
    #             time.sleep(10)
    #             print('[4Error] {} {} => {}'.format(j, self.raw_url, str(e)))
    #             break
    #         self.alldays.append([self.city, date, htemp, ltemp, status, winddir, windpower, self.updatetime])
    #     self.writeoutput()
    #
    def getCityData(self, city, raw_url):
        data = []
        url = Request(raw_url)
        url.add_header('User-Agent', 'Mozilla/5.0 Chrome/55.0.2883.95 Safari/{}.36'.format(random.randint(0, 30)))
        url.add_header('Referer', raw_url)
        try:
            raw = urlopen(url)
            res = BeautifulSoup(raw.read(), "lxml", from_encoding="GBK")
            for i in range(1,7):
                try:
                    raw_data = res.select('#detail')[0].select('div:nth-of-type({})'.format(i))[0]
                    tmp_date = datetime.date.today() + datetime.timedelta(days=(i-1))
                    date = tmp_date.strftime("%Y-%m-%d")
                    htemp = raw_data.select('ul > li:nth-of-type(2)')[0].text.replace('℃','').split('~')[0]
                    ltemp = raw_data.select('ul > li:nth-of-type(2)')[0].text.replace('℃','').split('~')[1]
                    status = raw_data.select('ul > li:nth-of-type(3)')[0].text
                    winddir = raw_data.select('ul > li:nth-of-type(4)')[0].text.split(' ')[0]
                    windpower = raw_data.select('ul > li:nth-of-type(4)')[0].text.split(' ')[1]
                    day = [city, date, htemp, ltemp, status, winddir, windpower, self.updatetime]
                    data.append(["{}".format(x) for x in day])

                except Exception as e:
                    print('[get data fail] {} => {}'.format(raw_url, str(e)))
                    # time.sleep(random.randint(0, 30))
                    # sys.exit()
            # print(raw.status)
            # print(raw.getheaders())
            return data
        except Exception as e:
            print('[open page fail] {} => {}'.format(raw_url, str(e)))
            # sys.exit()
        # print('[Done] - {} '.format(self.city))
        # self.writeoutput()

    def getCities(self):
        raw = urlopen('http://www.tianqi.com/chinacity.html')
        raw_data = BeautifulSoup(raw.read(), "lxml", from_encoding="GBK")
        for i in raw_data.find_all("ul", {'class': 'bcity'}):
            for j in i.find_all('a'):
                url = j['href']
                if url == '#':
                    continue
                else:
                    tmp = url.split('/')
                    city = None
                    if len(tmp) == 5:
                        city = tmp[3]
                    elif len(tmp) == 4:
                        city = tmp[2].split('.')[0]
                    self.cities.append((city, url))
                    # que.put(Job(city, url))
#
# class Job(object):
#     def __init__(self, city, url):
#         self.city = city
#         self.url = url
#
#     def do(self):
#         Spider(self.city, '{}7'.format(self.url)).getdata()
#
#     def no7(self):
#         Spider(self.city, self.url).getno7()
#
# def doJob(*args):
#     st = datetime.datetime.now()
#     # time.sleep(random.randint(0, 2))
#     queue = args[0]
#     while queue.qsize() > 0:
#         job = queue.get()
#         # job.do()
#         job.no7()
#     et = datetime.datetime.now()
#     print("[{}] Spending time={}!".format(threading.current_thread().name, (et - st).seconds))
#
#
# def printformat(msg):
#     print("~~~~~~~~~~~~~~{}~~~~~~~~~~~~~".format(msg))

#
# if __name__ == "__main__":
#     datatype = "7days"
#     dir_path = os.path.dirname(os.path.realpath('__file__'))
#     datadir = '{}/{}'.format(dir_path, datatype)
#     threads = []
#     cities = getCities()
#
#     que = addweatherjob(cities)
#
#     if not os.path.exists(datadir):
#         os.makedirs(datadir)
#
#     for j in range(30):
#         t = threading.Thread(target=doJob, name='Doer{}'.format(j), args=(que,))
#         threads.append(t)
#         t.start()

        # print('add {} threads to run'.format(len(threads)))
