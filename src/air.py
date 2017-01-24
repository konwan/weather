#!/usr/bin/env python
# -*- coding: utf-8 -*-
#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
from outputdata import OutputData
import io
from time import gmtime, strftime


class HistoryAir(OutputData):
    def __init__(self, *args, **kwargs):
        super(HistoryAir, self).__init__(*args, **kwargs)
        self.datatype = "air"
        self.updatetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.dir_path = os.path.dirname(os.path.realpath('__file__'))

    def getCityData(self, city, month):
        data = []
        url = Request('http://www.tianqihoubao.com/aqi/{}-{}.html'.format(city, month))
        url.add_header('User-Agent', 'Mozilla/5.0 Chrome/55.0.2883.95 Safari/{}.36'.format(random.randint(0, 30)))

        try:
            monthdata = urlopen(url)
            temp = BeautifulSoup(monthdata.read(), "lxml", from_encoding="GBK")
            temp_data = []
            temp_data_all = temp.find(id='bd').find_all('tr')
            if temp_data_all is not None:
                for k in temp_data_all:
                    data.append(["{}".format(x.text.strip().replace('\n','').replace('\r','')) for x in k.find_all('td')] + [city, self.updatetime])
        except Exception as e:
            print('[get data fail] {} => {}'.format(url, str(e)))

        return data


def getCities(ctid="citychk", alldate=False):
    skip = ['aqi_rank']
    checknum = 32
    lastmonth = datetime.datetime.now()+relativedelta(months=-1)
    cal_mon = lastmonth.strftime("%Y%m")
    dates = [cal_mon]
    all = alldate
    citiesid = ctid
    cities = []
    url = 'http://www.tianqihoubao.com/aqi/'
    response = urlopen(url)
    soup1 = BeautifulSoup(response.read(), "lxml", from_encoding="GBK")
    tmpcities = soup1.find('div',class_=ctid).find_all('a')
    for j, i in enumerate(tmpcities[0:20]):
        if i not in ['aqi_rank']:
            c_city = i.text
            e_city = i['href'].split('.')[0].split('/')[2]
            # if len(os.listdir('{}/{}/{}'.format(dir_path, datatype, i['href'].split('.')[0].split('/')[2]))) != checknum:
            #     skip.append(i['href'].split('.')[0].split('/')[2])
            # if e_city in skip:
            #     continue
            if all :
                try :
                    raw_date = urlopen('http://www.tianqihoubao.com/aqi/{}.html'.format(e_city))
                    bs4_date = BeautifulSoup(raw_date.read(), "lxml", from_encoding="GBK")
                except Exception as e:
                    print("{}  {}".format(e_city, str(e)))
                tmp = bs4_date.find('div',class_='box p')
                if tmp is None:
                    continue

                raw_dates = tmp.find_all('a')
                dates = [j['href'].split('.')[0].split('/')[2].split('-')[1] for j in raw_dates]

            for y in dates:
                cities.append((e_city, y))
    return cities

if __name__ == "__main__":
    t = HistoryAir()
    t.quote = False
    a = getCities(alldate=True)
    # print(a[0:4])
    city = 'beijing'
    month = '201612'
    for i in a[0:20] :
        city = i[0]
        month = i[1]
        datadir = "data/{}/{}".format(t.datatype, city)
        fn = '{}/{}-{}.csv'.format(datadir, city, month)
        data = t.getCityData(city, month)
        t.outputData(datadir, fn, data)
