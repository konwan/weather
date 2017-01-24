#!/usr/bin/env python
#-*- coding: utf-8 -*-

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
        self.today = datetime.datetime.now().strftime("%Y%m%d")
        self.updatetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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

            return data
        except Exception as e:
            print('[open page fail] {} => {}'.format(raw_url, str(e)))

def getCities():
    cities = []
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
                cities.append((city, url))
    return cities
