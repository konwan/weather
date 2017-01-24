#!/usr/bin/env python
#-*- coding: utf-8 -*-
import time
import queue
import datetime
import threading
import random
import os, sys

class AllSpiderJobs(object):
    def __init__(self, thread_cnt=30):
        self.thread_cnt = thread_cnt
        self.threads = []
        self.jobque = queue.Queue()
        self.jobs = None

    def addThread(self):
        for j in range(self.thread_cnt):
            t = threading.Thread(target=self.doJob, name='Doer{}'.format(j)) #, args=(aj.jobque,))
            self.threads.append(t)
            t.start()

    def addJob(self):
        for i, x in enumerate(self.jobs):
            city = i
            url = i
            self.jobque.put(SpiderJob(city, url))

    def doJob(self):
        st = datetime.datetime.now()
        while self.jobque.qsize() > 0:
            job = self.jobque.get()
            job.getdata()
        et = datetime.datetime.now()
        totalsec = (et - st).seconds
        print("[{}] Spending time={}!".format(threading.current_thread().name, totalsec))

class SpiderJob(object):
    def __init__(self, city, url='', getdatatime=''):
        self.city = city
        self.url = url
        self.getdatatime = getdatatime

    def getdata(self):
        time.sleep(3)
        # time.sleep(random.randint(0, 2))
        print(self.city, self.url)

    def __repr__(self):
        return "<Job(url='{}')>".format(self.url)
