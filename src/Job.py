# -*- coding: UTF-8 -*-
import time
import queue
import datetime
import threading
import random
import os, sys


class Job(object):
    def __init__(self, city, url):
        self.city = city
        self.url = url
        
    def history(self):
        HistoryWeather(self.city, self.month).getdata()

    def daily(self):
        DailyWeather().getDataMulti(self.city)

    def forecast(self):
        ForecastWeather(self.city, self.url).getno7()


def addjob(cities):
    que = queue.Queue()
    for i, x in enumerate(cities):
        if type == "daily" :
            print("[DW] - {}, {}".format(i, x))
            que.put(Job(x))
        if type == "forecast"
            url = '{}'.format(x['href'])
            tmp = url.split('/')
            city = None
            if len(tmp) == 5:
                city = tmp[3]
            elif len(tmp) == 4:
                city = tmp[2].split('.')[0]
            que.put(Job(city, url))
        if type == "history":
            if x['href'] != '#':
                ename = x['href'].split("/")[3]
                cname = x.string

                if ename in finished:
                    continue

                print(i, ename)
                dates = ['201612']
                datadir = "data/{}/{}".format(datatype, ename)

                if not os.path.exists(datadir):
                    os.makedirs(datadir)

                for y in dates:
                    que.put(Job(ename, y))
    return que




def doJob(*args):
    st = datetime.datetime.now()
    # time.sleep(random.randint(0, 2))
    queue = args[0]
    while queue.qsize() > 0:
        job = queue.get()
        # job.do()
        job.no7()
    et = datetime.datetime.now()
    print("[{}] Spending time={}!".format(threading.current_thread().name, (et - st).seconds))


if __name__ == '__main__':
    # set jo to que
    que = addjob(cities)
    # new thread to dojob
    threads = []
    for j in range(30):
        t = threading.Thread(target=doJob, name='Doer{}'.format(j), args=(que,))
        threads.append(t)
        t.start()
