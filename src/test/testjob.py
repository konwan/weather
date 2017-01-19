# -*- coding: UTF-8 -*-

import os
import sys
import unittest
import datetime
import threading
# sys.path.append("/Users/data/Desktop/cindy/weather")
# sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from job.spiderjob import AllSpiderJobs, SpiderJob
from historyweather import HistoryWeather
from forecast import ForecastWeather
from urllib.request import urlopen, Request, urlretrieve


# if __name__ == "__main__":
#     print(sys.path)
#     print(SpiderJob('','oeoiw'))
#     print('nono')

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

    # def test_daily(self):
    #     pass
    #
    # def test_forecast(self):
    #     pass
    #
    # def test_history(self):
    #     pass
    #
    def tearDown(self):
        pass

class TestHis(unittest.TestCase):
    def setUp(self):
        self.his = HistoryWeather()
        self.his.all = True
        self.his.quote = True
        self.his.citiesid = "city_O"
        self.city = "ouhaiqu"
        self.month = "201610"
        self.data = []
        self.datadir = "data/{}/{}".format(self.his.datatype, self.city)
        self.fn = "{}/{}_{}.csv".format(self.datadir, self.city, self.month)

    def test_outputdata(self):
        self.data = self.his.getCityData(self.city, self.month)
        self.his.outputData(self.datadir, self.fn, self.data)
        self.assertEqual(os.path.exists(self.fn) , True)
        print("[{}: {}] - {} ".format(self.__class__.__name__, self.test_outputdata.__name__, self.fn))

    def test_getcities(self):
        self.his.getCities()
        tmpcts = len(self.his.cities)
        self.assertEqual(tmpcts , len(self.his.dates))
        print("[{}: {}] - total {} tasks!".format(self.__class__.__name__, self.test_getcities.__name__, tmpcts))

    def test_getcitydata(self):
        self.data = self.his.getCityData(self.city, self.month)
        self.assertEqual(len(self.data) , 32)
        print("[{}: {}] -  {} !".format(self.__class__.__name__, self.test_getcitydata.__name__, self.fn))

class TestFcast(unittest.TestCase):
    def setUp(self):
        self.fc = ForecastWeather()
        self.fc.quote = True
        self.cities = [('acheng', 'http://haerbin.tianqi.com/acheng/'), ('angangxiqu', 'http://qiqihaer.tianqi.com/angangxiqu/')]
        self.city = 'angangxiqu'
        self.url = 'http://qiqihaer.tianqi.com/angangxiqu/'
        self.data = []
        self.datadir = "data/{}/{}".format(self.fc.datatype, self.city)
        self.fn = "{}/{}_{}.csv".format(self.datadir, self.city, self.fc.today)

    def test_getcitydata(self):
        self.data = self.fc.getCityData(self.city, self.url)
        self.fc.outputData(self.datadir, self.fn, self.data)

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

    # def test_getcities(self):
    #     self.fc.getCities()
    #     self.assertEqual(self.fc.cities[0][0] , 'acheng')
    #     print("[{}: {}] - total {} tasks!".format(self.__class__.__name__, self.test_getcities.__name__, len(self.fc.cities)))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFcast)
    unittest.TextTestRunner(verbosity=2).run(suite)
    # verbosity shows test_getcities (__main__.TestHis) ... ok insteat of .
    # unittest.main()
    # python -m unittest testMyCase.MyCase.testItIsHot