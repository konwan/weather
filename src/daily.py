#!/usr/bin/env python
#-*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.select import Select
import os
from bs4 import BeautifulSoup
import time
import queue
import datetime
import threading
import random

class DailyWeather(object):
    def __init__(self):
        # self.phantomjs_path = r"/Users/data/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs"
        self.url = "http://tianqi.2345.com/wea_history/71294.htm"
        self.agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0 "
        #self.dir_path = os.path.dirname(os.path.realpath('__file__'))
        self.dir_path = "/opt/weather"
        self.phantomjs_path = r"{}/phantomjs/bin/phantomjs".format(self.dir_path)
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
        # print("[DW] - customerize header")
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (self.agent)
        dcap["phantomjs.page.customHeaders.Referer"] = (self.url)
        # headers = {"Referer": self.url, "User-Agent": self.agent}
        # for key, value in enumerate(headers):
        #     DesiredCapabilities.PHANTOMJS["phantomjs.page.customHeaders.{}".format(key)] = value
        self.driver = webdriver.PhantomJS(desired_capabilities=dcap, executable_path=self.phantomjs_path)
        # cap_dict = self.driver.desired_capabilities
        # for key in cap_dict:
        #     print(key, cap_dict[key])

    def checkDir(self):
        if not os.path.exists(self.datadir):
            os.makedirs(self.datadir)

    def outputFile(self, data):
        self.checkDir()
        print(self.dir_path)
        file = open(self.filename, 'w')
        for i in data:
            if self.quote :
                result = ["'{}'".format(x) for x in i]
            else :
                result = i
            file.write("{}\n".format(",".join(result)))
        file.close()


    def getGeoData(self):
        self.datadir = '{}/data/{}'.format(self.dir_path, self.datatype)
        self.filename = '{}/wea2345_city.csv'.format(self.datadir)
        self.cusHeader()
        print("[DW] - start get geodata")
        print("[DW] - {}".format(self.url))
        self.driver.get(self.url)
        print("[DW] - {}".format(self.driver))
        self.driver.find_element_by_css_selector("#switchHisCity").click()
        provs = [x for x in self.driver.find_elements_by_css_selector("#selectProv > option:nth-of-type(31)")]
        print("[DW] - {}".format(provs))
        for i in provs:
            print("[DW] - {} {}".format(i.text, i.get_attribute('value')))
            self.driver.find_element_by_css_selector("#selectProv > option[value='{}']".format(i.get_attribute('value'))).click()
            cities = [x for x in self.driver.find_elements_by_css_selector("#chengs_ls > option")]
            for j in cities:
                self.driver.find_element_by_css_selector("#chengs_ls > option[value='{}']".format(j.get_attribute('value'))).click()
                areas = [x for x in self.driver.find_elements_by_css_selector("#cityqx_ls > option")]
                for m, k in enumerate(areas) :
                    tmp = [i.text, j.text, k.text, i.get_attribute('value'), j.get_attribute('value'), k.get_attribute('value')]
                    flattmp = [j for i in tmp for j in i.split(' ')]
                    self.geo.append(flattmp)
        if self.outputlist:
            self.outputFile(self.geo)


    def getData(self):
        print(self.geo)
        # self.geo = ['X', '香港', 'X', '香港', 'X', '香港', '39', '39,0', '45007']
        for m, i in enumerate(self.geo):
            print("[DW] - start get [{} {} {}] data".format(i[1], i[3], i[5]))
            self.url = "http://tianqi.2345.com/wea_history/{}.htm".format(i[8])
            self.agent = "Mozilla/{} (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0 ".format(m)
            self.cusHeader()
            print(self.url)
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

                self.data.append([tmp[0], tmp[1][0:10], tmp[2], tmp[3], tmp[5][0:winsep(tmp[5])], tmp[5][winsep(tmp[5]):], tmp[6][0:airsep(tmp[6])], tmp[6][airsep(tmp[6]):]])
                # ['2017-01-01星期日', '14', '4', '多云', '东北风1-2级', '196中度污染']
        print(self.data)
        self.driver.close()  # 關閉瀏覽器


    def getDataMulti(self, city):
        i = city
        today = datetime.datetime.now()
        month = (today - datetime.timedelta(days=1)).strftime("%Y%m")
        self.datadir = '{}/data/{}/{}'.format(self.dir_path, self.datatype, i[8])
        self.filename = '{}/{}_{}.csv'.format(self.datadir, i[8], month)
        # self.geo = ['X', '香港', 'X', '香港', 'X', '香港', '39', '39,0', '45007']

        print("[DW-{}] - start get [{} {} {}] data".format(threading.current_thread().name, i[1], i[3], i[5]))
        self.url = "http://tianqi.2345.com/wea_history/{}.htm".format(i[8])
        self.agent = "Mozilla/{} (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0 ".format(random.randint(0, 2))
        self.cusHeader()
        self.driver.get(self.url)
        # add try exception
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
            # ['2017-01-01星期日', '14', '4', '多云', '东北风1-2级', '196中度污染']
        # print(self.data)
        self.driver.close()  # 關閉瀏覽器
        self.outputFile(self.data)


    def __repr__(self):
        # return '<DailyWeather>'
        return "<DailyWeather(url='{}')>".format(self.driver.current_url)

class Job(object):
    def __init__(self, city):
        self.city = city

    def daily(self):
        DailyWeather().getDataMulti(self.city)


def dailyweather(cities):
    que = queue.Queue()
    for m, i in enumerate(cities):
        print("[DW] - {}, {}".format(m, i))
        que.put(Job(i))
    return que

def doJob(*args):
    st = datetime.datetime.now()
    # time.sleep(random.randint(0, 2))
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

    for j in range(2):
        t = threading.Thread(target=doJob, name='Doer{}'.format(j), args=(que,))
        threads.append(t)
        t.start()

