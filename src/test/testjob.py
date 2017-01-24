#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys
import unittest
import datetime
import threading
import random
import time
# sys.path.append("/Users/data/Desktop/cindy/weather")
# sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from job.spiderjob import AllSpiderJobs
from history import HistoryWeather, getCities as hisgetCities
from forecast import ForecastWeather, getCities as forgetCities
from daily import DailyWeather


class TestJob(unittest.TestCase):
    def setUp(self):
        self.aj = AllSpiderJobs(thread_cnt=3)
        self.aj.city = "cindy_city"
        self.aj.url = "test test"
        self.aj.jobs = ['cindy', 'jeremy', 'sjz']

    def test_addjb(self):
        self.aj.addJob()
        self.assertEqual(self.aj.jobque.qsize() , len(self.aj.jobs))
        print("[{}: {}] - all tasks in que {}".format(self.__class__.__name__, self.test_addjb.__name__, self.aj.jobque.queue))

    def test_dojob(self):
        self.aj.addJob()
        self.aj.doJob()
        self.assertEqual(self.aj.jobque.qsize() , 0)
        print("[{}: {}] - {} done!".format(self.__class__.__name__, self.test_dojob.__name__, threading.current_thread().name))

    def test_addthread(self):
        self.aj.addJob()
        self.aj.addThread()
        self.assertEqual(self.aj.jobque.qsize() , 0)
        print("[{}: {}] - {} finished!".format(self.__class__.__name__, self.test_addthread.__name__, threading.current_thread().name))

    def tearDown(self):
        pass

class TestHis(unittest.TestCase):
    def setUp(self):
        self.his = HistoryWeather()
        self.his.quote = True
        self.all = False
        self.city = "ouhaiqu"
        self.citiesid = "city_P"
        self.month = "201610"
        self.dates = [self.month]
        self.data = []
        self.datadir = "data/{}/{}".format(self.his.datatype, self.city)
        self.fn = "{}/{}_{}.csv".format(self.datadir, self.city, self.month)

    def test_getcities(self):
        st = datetime.datetime.now()
        cities = hisgetCities(ctid=self.citiesid, alldate=self.all)
        et = datetime.datetime.now()
        tmpcts = len(cities)
        self.assertEqual(tmpcts , tmpcts)
        print("[{}: {}] - total {} tasks {} secs!".format(self.__class__.__name__, self.test_getcities.__name__, tmpcts, (et - st).seconds))

    def test_outputdata(self):
        cities = hisgetCities(ctid=self.citiesid, alldate=self.all)
        st = datetime.datetime.now()
        for i in cities[0:5]:
            tmpcy = i[0]
            tmpmon = i[1]
            time.sleep(random.randint(0, 2))
            self.data = self.his.getCityData(tmpcy, tmpmon)
            self.datadir = "data/{}/{}".format(self.his.datatype, tmpcy)
            self.fn = "{}/{}_{}.csv".format(self.datadir, tmpcy, tmpmon)
            self.his.outputData(self.datadir, self.fn, self.data)
            self.assertEqual(os.path.exists(self.fn) , True)
            print("[{}: {}] - {} ".format(self.__class__.__name__, self.test_outputdata.__name__, self.fn))
        et = datetime.datetime.now()
        print("[{}: {}] - total {} ".format(self.__class__.__name__, self.test_outputdata.__name__, (et - st).seconds))

    def test_getcitydata(self):
        st = datetime.datetime.now()
        self.data = self.his.getCityData(self.city, self.month)
        et = datetime.datetime.now()
        self.assertEqual(len(self.data) , 32)
        print("[{}: {}] -  {} cost {} secs !".format(self.__class__.__name__, self.test_getcitydata.__name__, self.fn, (et - st).seconds))

class TestFcast(unittest.TestCase):
    def setUp(self):
        self.fc = ForecastWeather()
        # self.fc.quote = True
        self.cities = [('acheng', 'http://haerbin.tianqi.com/acheng/'), ('angangxiqu', 'http://qiqihaer.tianqi.com/angangxiqu/')]
        self.city = 'angangxiqu'
        self.url = 'http://qiqihaer.tianqi.com/angangxiqu/'
        self.data = []
        self.datadir = "data/{}/{}".format(self.fc.datatype, self.city)
        self.fn = "{}/{}_{}.csv".format(self.datadir, self.city, self.fc.today)

    def test_getcitydata(self):
        st = datetime.datetime.now()
        self.data = self.fc.getCityData(self.city, self.url)
        et = datetime.datetime.now()
        self.fc.outputData(self.datadir, self.fn, self.data)
        self.assertEqual(os.path.exists(self.fn) , True)
        print("[{}: {}] - {} cost {} secs!".format(self.__class__.__name__, self.test_getcitydata.__name__, self.fn, (et - st).seconds))

        # raw_url = 'https://www.python.org'
        # url = Request(raw_url)
        # url.add_header('User-Agent', 'Mozilla/5.0 Chrome/55.0.2883.95 Safari/{}.36'.format("777"))
        # url.add_header('Referer', raw_url)
        # url.add_unredirected_header('User-Agent', 'Mozilla/5.0 Chrome/55.0.2883.95 Safari/{}.36'.format("777"))
        #
        # response = urlopen(url)
        # print(response.status)
        # print(response.getheader('Server'))
        # print(response.getheaders())

    def test_getcities(self):
        st = datetime.datetime.now()
        self.cities = forgetCities()
        et = datetime.datetime.now()
        self.assertEqual(self.cities[0][0] , 'acheng')
        print("[{}: {}] - total {} tasks {} secs!".format(self.__class__.__name__, self.test_getcities.__name__, len(self.cities), (et - st).seconds))

class TestDaily(unittest.TestCase):
    def setUp(self):
        self.dw = DailyWeather()
        self.dw.quote = True
        # self.dw.browser = "chrome"
        self.dw.cssprov = "#selectProv > option:nth-of-type(24)"
        self.dw.csscity = "#chengs_ls > option:nth-of-type(11)"
        self.geo = []
        self.driver = None
        #self.city = ['S', '山西', 'Y', '运城', 'Y', '永济', '32', '32,10', '60235']
        self.city = ['X', '香港', 'X', '香港', 'X', '香港', '39', '39,0', '45007']
        self.data = []
        self.today = datetime.datetime.now()
        self.month = (self.today - datetime.timedelta(days=1)).strftime("%Y%m")
        self.datadir = "data/{}/{}".format(self.dw.datatype, self.city[8])
        self.fn = "{}/{}_{}.csv".format(self.datadir, self.city[8], self.month)

    # def test_header(self):
        # self.driver = self.dw.cusHeader()
        # cap_dict = self.driver.desired_capabilities
        # self.assertEqual(cap_dict['phantomjs.page.customHeaders.Referer'] , self.dw.tmpurl)
        # print("[{}: {}] - Referer => {}".format(self.__class__.__name__, self.test_header.__name__, self.dw.tmpurl))
        # for key in cap_dict:
        #     print("[header] - {}: {}".format(key, cap_dict[key]))

    def test_getcitydata(self):
        st = datetime.datetime.now()
        self.data = self.dw.getCityData(self.city)
        et = datetime.datetime.now()
        self.dw.outputData(self.datadir, self.fn, self.data)
        self.assertEqual(os.path.exists(self.fn) , True)
        print("[{}: {}] - {} with {} secs!".format(self.__class__.__name__, self.test_getcitydata.__name__, self.fn, (et - st).seconds))

    def test_getcities(self):
        st = datetime.datetime.now()
        self.cities = self.dw.getCities()
        et = datetime.datetime.now()
        self.assertEqual(self.cities[0][8] , '60236')
        print("[{}: {}] - get {} cities with {} secs!".format(self.__class__.__name__, self.test_getcities.__name__, len(self.cities), (et - st).seconds))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDaily)
    unittest.TextTestRunner(verbosity=2).run(suite)
    # verbosity shows test_getcities (__main__.TestHis) ... ok insteat of .
    # unittest.main()
    # python -m unittest testMyCase.MyCase.testItIsHot
