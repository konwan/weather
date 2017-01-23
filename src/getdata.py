# -*- coding: UTF-8 -*-
import os
import sys
import queue
from queue import Empty
import threading
import random
import datetime
import time
from job.spiderjob import AllSpiderJobs
from history import HistoryWeather, getCities as hisgetCities
from forecast import ForecastWeather, getCities as forgetCities
from daily import DailyWeather

class HisJob(object):
    def __init__(self, city, month):
        self.city = city
        self.month = month
        self.datatype = "history"
        self.datadir = "data/{}/{}".format(self.datatype, self.city)
        self.today = datetime.datetime.now().strftime("%Y%m%d")
        self.fn = "{}/{}_{}.csv".format(self.datadir, self.city, self.month)

    def do(self):
        hw = HistoryWeather()
        data = hw.getCityData(self.city, self.month)
        hw.outputData(self.datadir, self.fn, data)

class ForJob(object):
    def __init__(self, city, url):
        self.city = city
        self.url = url
        self.datatype = "shit"
        self.datadir = "data/{}/{}".format(self.datatype, self.city)
        self.today = datetime.datetime.now().strftime("%Y%m%d")
        self.fn = "{}/{}_{}.csv".format(self.datadir, self.city, self.today)

    def do(self):
        fw = ForecastWeather()
        data = fw.getCityData(self.city, self.url)
        fw.outputData(self.datadir, self.fn, data)

class DalJob(object):
    def __init__(self, city):
        self.city = city
        self.datatype = "daily"
        self.datadir = "data/{}/{}".format(self.datatype, self.city[8])
        self.today = datetime.datetime.now()
        self.month = (self.today - datetime.timedelta(days=1)).strftime("%Y%m")
        self.fn = "{}/{}_{}.csv".format(self.datadir, self.city[8], self.month)

    def do(self):
        dw = DailyWeather()
        data = dw.getCityData(self.city)
        dw.outputData(self.datadir, self.fn, data)

def doJob(*args):
    st = datetime.datetime.now()
    que = args[0]
    while que.qsize() > 0:
        time.sleep(random.randint(0, 2))
        try:
            job = que.get(block=True, timeout=0.1)
            job.do()
        except Empty:
            pass
    et = datetime.datetime.now()
    # is_main_thread_active = lambda : any((i.name == "MainThread") and i.is_alive() for i in threading.enumerate())
    # print(is_main_thread_active())
    print("[{}] Spending time={}!".format(threading.current_thread().name, (et - st).seconds))


if __name__ == "__main__":
    type = sys.argv[1]
    threads = []
    que = queue.Queue()
    thread_cnt = 10

    if type == "daily":
        dwo = DailyWeather()
        # dwo.browser = "chrome"
        # dwo.cssprov = "#selectProv > option:nth-of-type(31)"
        # dwo.csscity = "#chengs_ls > option:nth-of-type(11)"
        cities = dwo.getCities()
        for i in cities:
            que.put(DalJob(i))

    elif type == "forecast":
        cities = hisgetCities()
        for i in cities:
            que.put(HisJob(i[0], i[1]))

    elif type == "history":
        cities = forgetCities()
        for i in cities:
            que.put(ForJob(i[0], i[1]))

    else:
        print("enter a type  daily| forecast| history")
        sys.exit()
    for j in range(thread_cnt):
        t = threading.Thread(target=doJob, name='Doer{}'.format(j), args=(que,))
        threads.append(t)
        t.start()
        # t.join(timeout=1)
