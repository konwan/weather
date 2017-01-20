# -*- coding: UTF-8 -*-
import os
import sys
import datetime
import time
from job.spiderjob import AllSpiderJobs
from history import HistoryWeather
from forecast import ForecastWeather
# from daily import DailyWeather

class HisJobs(AllSpiderJobs):
    def __init__(self, *args, **kwargs):
        super(HisJobs, self).__init__(*args, **kwargs)
        # def __init__(self, thread_cnt=30):
        self.hw = HistoryWeather()
        self.hw.citiesid = "city_O"
        self.hw.all = True
        self.hw.getCities()
        self.jobs = self.hw.cities

    def addJob(self):
        for i, x in enumerate(self.jobs):
            city = x[0]
            month = x[1]
            self.jobque.put(self.hw.getCityData(city, month))

    def doJob(self):
        st = datetime.datetime.now()
        while self.jobque.qsize() > 0:
            job = self.jobque.get()
            # job.getdata()
        et = datetime.datetime.now()
        totalsec = (et - st).seconds
        print("[{}] Spending time={}!".format(threading.current_thread().name, totalsec))


class ForJobs(AllSpiderJobs, ForecastWeather):
    def __init__(self, *args, **kwargs):
        super(ForJobs, self).__init__(*args, **kwargs)
        self.jobs = self.getCities()

    def addJob(self):
        for i, x in enumerate(self.jobs):
            city = x[0]
            url = x[1]
            self.jobque.put(self.getCityData(city, url))

    def doJob(self):
        st = datetime.datetime.now()
        while self.jobque.qsize() > 0:
            job = self.jobque.get()
            # self.outputData(self.datadir, self.fn, self.data)
        et = datetime.datetime.now()
        totalsec = (et - st).seconds
        print("[{}] Spending time={}!".format(threading.current_thread().name, totalsec))
# class DoSpiderJob(object):
#     def __init__(self, type='history', city='', url='', getdatatime=''):
#         self.type = type
#         self.city = city
#         self.url = url
#         self.getdatatime = getdatatime
#
#     def getdata(self):
#         his = HistoryWeather()
#         his.getCities()
#         cts = HistoryWeather.getdata()
#         time.sleep(random.randint(0, 2))
#         print(self.city, self.url)
#
#     # def __repr__(self):
#     #     return "<Job(url='{}')>".format(self.url)
#     # # def history(self):
#     # #     HistoryWeather(self.city, self.month).getdata()
#     # self.data = self.his.getCityData(tmpcy, tmpmon)
#     # #
#     # # def daily(self):
#     # #     DailyWeather().getDataMulti(self.city)
#     # self.data = self.dw.getDataMulti(self.city)
#     # #
#     # # def forecast(self):
#     # #     ForecastWeather(self.city, self.url).getno7()
#     # self.data = self.fc.getCityData(self.city, self.url)


if __name__ == "__main__":
    # h = HisJobs()
    # h.addJob()
    # h.addThread()
    # f = ForJobs()
    # f.addJob()
    # # f.doJob()
    # f.addThread()
    pass
