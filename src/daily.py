#!/usr/bin/env python
#-*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.select import Select
import os
import sys
from bs4 import BeautifulSoup
import time
import queue
import datetime
import threading
import random

class DailyWeather(object):
    def __init__(self):
        self.phantomjs_path = r"/Users/data/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs"
        self.url = "http://tianqi.2345.com/wea_history/71294.htm"
        self.agent = "Mozilla/{x}.0 (Macintosh; Intel Mac OS X 10.9; rv:{x}.0) Firefox/{x}.0".format(x=random.randint(0,30))
        # Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36
        self.dir_path = os.path.dirname(os.path.realpath('__file__'))
        self.datatype = "daily"
        self.datadir = None
        self.filename = None
        self.quote = False
        self.outputlist = False
        self.driver = None
        self.geo = []
        self.data = []
        self.day = []
        # self.getGeoData()

    def cusHeader(self):
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (self.agent)
        dcap["phantomjs.page.customHeaders.Referer"] = (self.url)
        self.driver = webdriver.PhantomJS(desired_capabilities=dcap, executable_path=self.phantomjs_path)

        #self.driver.add_cookie({'Accept-Encoding':'gzip, deflate, sdch', 'User-Agent':self.agent})

    def checkDir(self):
        if not os.path.exists(self.datadir):
            os.makedirs(self.datadir)

    def outputFile(self, data):
        self.checkDir()
        file = open(self.filename, 'w')
        for i in data:
            if self.quote :
                result = ["'{}'".format(x) for x in i]
            else :
                result = i
            file.write("{}\n".format(",".join(result)))
        file.close()

    def getGeoData(self):
        self.datadir = '{}/{}'.format(self.dir_path, self.datatype)
        self.filename = '{}/wea2345_city.csv'.format(self.datadir)
        self.cusHeader()
        print("[DW] - start get geodata")
        self.driver.get(self.url)
        self.driver.find_element_by_css_selector("#switchHisCity").click()
        provs = [x for x in self.driver.find_elements_by_css_selector("#selectProv > option:nth-of-type(24)")] # :nth-of-type(31)
        for i in provs:
            # print("[DW] - {}".format(i))
            self.driver.find_element_by_css_selector("#selectProv > option[value='{}']".format(i.get_attribute('value'))).click()
            cities = [x for x in self.driver.find_elements_by_css_selector("#chengs_ls > option:nth-of-type(11)")] # :nth-of-type(11)
            for j in cities:
                self.driver.find_element_by_css_selector("#chengs_ls > option[value='{}']".format(j.get_attribute('value'))).click()
                areas = [x for x in self.driver.find_elements_by_css_selector("#cityqx_ls > option")]
                for m, k in enumerate(areas) :
                    tmp = [i.text, j.text, k.text, i.get_attribute('value'), j.get_attribute('value'), k.get_attribute('value')]
                    flattmp = [j for i in tmp for j in i.split(' ')]
                    self.geo.append(flattmp)
        self.driver.close()
        if self.outputlist:
            self.outputFile(self.geo)

    def getDataMulti(self, city, retry=0):
        time.sleep(random.randint(0, 2))
        i = city
        today = datetime.datetime.now()
        month = (today - datetime.timedelta(days=1)).strftime("%Y%m")
        self.datadir = '{}/{}/{}'.format(self.dir_path, self.datatype, i[8])
        self.filename = '{}/{}_{}.csv'.format(self.datadir, i[8], month)

        print("[DW-{}] - start get [{} {} {}] data".format(threading.current_thread().name, i[1], i[3], i[5]))
        self.url = "http://tianqi.2345.com/wea_history/{}.htm".format(i[8])
        self.agent = "Mozilla/{x}.0 (Macintosh; Intel Mac OS X {x}.9; rv:{x}.0) Firefox/{x}.0".format(x=random.randint(0,10))
        self.cusHeader()
        if retry < 2 :
            try:
                self.driver.get(self.url)
                self.driver.find_element_by_css_selector("#switchHisCity").click() # click change city
                self.driver.find_element_by_css_selector("#selectProv > option[value='{}']".format(i[6])).click()
                self.driver.find_element_by_css_selector("#chengs_ls > option[value='{}']".format(i[7])).click()
                self.driver.find_element_by_css_selector("#cityqx_ls > option[value='{}']".format(i[8])).click()
                self.driver.find_element_by_css_selector('#buttonsdm_dz').click() # rerenden page
                res = BeautifulSoup(self.driver.page_source, "lxml")
                daydata = res.select('#weather_tab > table > tbody > tr')
                for l in daydata:
                    tmp = [i[8]]+[i.text.replace('℃','') for i in l.select('td')]
                    checkwin = [i for i in tmp[5] if i.isdigit()]
                    checkair = [i for i in tmp[6] if not i.isdigit()]
                    winsep = lambda x: x.index(checkwin[0]) if len(checkwin) > 0 else len(x)
                    airsep = lambda x: x.index(checkair[0]) if len(checkair) > 0 else len(x)
                    updatetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    daily = [tmp[0], tmp[1][0:10], tmp[2], tmp[3], tmp[5][0:winsep(tmp[5])], tmp[5][winsep(tmp[5]):], tmp[6][0:airsep(tmp[6])], tmp[6][airsep(tmp[6]):], updatetime]
                    self.data.append(daily)
                self.driver.quit()  # 關閉瀏覽器
                self.outputFile(self.data)
            except Exception as e:
                retry += 1
                time.sleep(25)
                self.getDataMulti(city, retry)
                print('[get data fail] {} => {}'.format(self.url, str(e)))
                sys.exit()

    def __repr__(self):
        return "<DailyWeather(url='{}')>".format(self.driver.current_url)

class Job(object):
    def __init__(self, city):
        self.city = city

    def daily(self):
        DailyWeather().getDataMulti(self.city)


def dailyweather(cities):
    que = queue.Queue()
    for m, i in enumerate(cities):
        # print("[DW] - {}, {}".format(m, i))
        que.put(Job(i))
    return que

def doJob(*args):
    st = datetime.datetime.now()
    queue = args[0]
    while queue.qsize() > 0:
        job = queue.get()
        job.daily()
    et = datetime.datetime.now()
    print("[{}] Spending time={}!".format(threading.current_thread().name, (et - st).seconds))


if __name__ == "__main__":
    threads = []
    dw = DailyWeather()
    dw.getGeoData()
    cities = dw.geo
    que = dailyweather(cities)

    for j in range(30):
        t = threading.Thread(target=doJob, name='Doer{}'.format(j), args=(que,))
        threads.append(t)
        t.start()
