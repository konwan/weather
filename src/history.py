#!/usr/bin/env python
#-*- coding: utf-8 -*-

import time
import queue
import datetime
import threading
import random
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from dateutil.relativedelta import relativedelta
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from job.spiderjob import AllSpiderJobs, SpiderJob
from outputdata import OutputData

class HistoryWeather(OutputData):
    def __init__(self, *args, **kwargs):
        super(HistoryWeather, self).__init__(*args, **kwargs)
        self.datatype = "history"
        self.updatetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.dir_path = os.path.dirname(os.path.realpath('__file__'))
        self.checknum = 71

    def getCityData(self, city, month):
        data = []
        datadir = "{}/{}".format(self.datatype, city)
        url = Request('http://lishi.tianqi.com/{}/{}.html'.format(city, month))
        url.add_header('User-Agent', 'Mozilla/5.0 Chrome/55.0.2883.95 Safari/{}.36'.format(random.randint(0, 30)))
        try:
            monthdata = urlopen(url)
            temp = BeautifulSoup(monthdata.read(), "lxml", from_encoding="GBK")
            temp_data = []
            data = []
            temp_data_all = temp.find("div", {'class': 'tqtongji2'})
            if temp_data_all is not None:
                temp_data = temp_data_all.find_all('ul')
                for i in temp_data:
                    data.append(["{}".format(x.text) for x in i.find_all('li')] + [city, self.updatetime])
        except Exception as e:
            print('[get data fail] {} => {}'.format(url, str(e)))
        return data


def getCities(ctid="tool_site", alldate=False):
    skip = ['bagong-mountainqu']
    lastmonth = datetime.datetime.now()+relativedelta(months=-1)
    cal_mon = lastmonth.strftime("%Y%m")
    dates = [cal_mon]
    all = alldate
    citiesid = ctid
    cities = []
    url = 'http://lishi.tianqi.com/'
    response = urlopen('http://lishi.tianqi.com/')
    soup1 = BeautifulSoup(response.read(), "lxml", from_encoding="GBK")
    tmpcities = soup1.find(id=citiesid).find_all('a')
    for i, x in enumerate(tmpcities):
        if x['href'] != '#':
            ename = x['href'].split("/")[3]
            cname = x.string

            if ename in skip:
                continue
            if all :
                daterange = urlopen('http://lishi.tianqi.com/{}/index.html'.format(ename))
                date = BeautifulSoup(daterange.read(), "lxml", from_encoding="GBK")
                dates = [x['value'] for x in date.find(id="tool_site").find_all('option') if x['value'] != ""]

            for y in dates:
                cities.append((ename, y))
    return cities
