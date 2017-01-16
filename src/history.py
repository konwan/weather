#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import queue
import datetime
import threading
import random
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import os


class Spider(object):
    def __init__(self, city, month):
        self.city = city
        self.month = month

    def getdata(self):
        datatype = "weather"
        datadir = "{}/{}".format(datatype, self.city)

        st = datetime.datetime.now()
        # time.sleep(random.uniform(0, 1))
        print('{}/{}_{}.csv'.format(datadir, self.city, self.month))
        url = Request('http://lishi.tianqi.com/{}/{}.html'.format(self.city, self.month))
        url.add_header('User-Agent', 'hello.com')
        monthdata = urlopen(url)
        temp = BeautifulSoup(monthdata.read(), "lxml", from_encoding="GBK")
        temp_data = []
        temp_data_all = temp.find("div", {'class': 'tqtongji2'})
        if temp_data_all is not None:
            temp_data = temp_data_all.find_all('ul')

        file = open('{}/{}_{}.csv'.format(datadir, self.city, self.month), 'w')

        for i in temp_data:
            day = ["'{}'".format(x.text) for x in i.find_all('li')] + ["'{}'".format(self.city)]
            file.write("{}\n".format(",".join(day)))
        file.close()

        et = datetime.datetime.now()
        # print("\t[{}] {}_{} is done, cost {}! ".format(threading.current_thread().name, self.city, self.month, (et - st).seconds))


class Job(object):
    def __init__(self, city, month):
        self.city = city
        self.month = month

    def do(self):
        Spider(self.city, self.month).getdata()


def doJob(*args):
    st = datetime.datetime.now()
    # time.sleep(random.randint(0, 2))
    queue = args[0]
    while queue.qsize() > 0:
        job = queue.get()
        job.do()
    et = datetime.datetime.now()
    print("[{}] Spending time={}!".format(threading.current_thread().name, (et - st).seconds))


if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath('__file__'))
    threads = []
    que = queue.Queue()

    response = urlopen('http://lishi.tianqi.com/')
    soup1 = BeautifulSoup(response.read(), "lxml", from_encoding="GBK")
    ctrys = soup1.find(id="tool_site").find_all('a')
    # ctrys = soup1.find(id="city_P")
    # citys = ctrys.find_all('a')
    # type = ctrys.attrs['id']
    citys = ctrys
    datatype = "weather"
    checknum = 71
    finished = ['bagong-mountainqu']
    # for i in citys:
    #     if i['href'] != '#':
    #         if not os.path.exists('{}/{}/{}'.format(dir_path, datatype, i['href'].split("/")[3])):
    #             os.makedirs('{}/{}/{}'.format(dir_path, datatype, i['href'].split("/")[3]))
    #         if len(os.listdir('{}/{}/{}'.format(dir_path, datatype, i['href'].split("/")[3]))) != checknum:
    #             finished.append(i['href'].split("/")[3])

    for i, x in enumerate(citys):
        if x['href'] != '#':
            ename = x['href'].split("/")[3]
            cname = x.string

            if ename in finished:
                continue

            print(i, ename)
            # daterange = urlopen('http://lishi.tianqi.com/{}/index.html'.format(ename))
            # date = BeautifulSoup(daterange.read(), "lxml", from_encoding="GBK")
            dates = ['201612']
            # dates = [x['value'] for x in date.find(id="tool_site").find_all('option') if x['value'] != ""]
            datadir = "{}/{}".format(datatype, ename)

            # z1 = date.select('select#province option[selected=""]')
            # z2 = date.select('select#city option[selected=""]')
            # z3 = date.select('select#zone option[selected=""]')
            # z1_e, z1_c, z1_g = '', '', ''
            # z2_e, z2_c, z2_g = '', '', ''
            # z3_e, z3_c, z3_g = '', '', ''
            #
            # if len(z1) != 0:
            #     z1_e = z1[0].attrs['py']
            #     z1_c = z1[0].text.split(' ')[1]
            #     z1_g = z1[0].text.split(' ')[0]
            # if len(z2) != 0:
            #     z2_e = z2[0].attrs['py']
            #     z2_c = z2[0].text.split(' ')[1]
            #     z2_g = z2[0].text.split(' ')[0]
            # if len(z3) != 0:
            #     z3_e = z3[0].attrs['py']
            #     z3_c = z3[0].text.split(' ')[1]
            #     z3_g = z3[0].text.split(' ')[0]
            #
            # file = open('{}/{}_city.csv'.format(dir_path, datatype), 'a')
            # geo = ("'{}','{}','{}','{}','{}','{}','{}','{}','{}'\n".format(z1_e, z2_e, z3_e, z1_c, z2_c, z3_c, z1_g, z2_g, z3_g))
            # file.write(geo)
            # file.close()

            if not os.path.exists(datadir):
                os.makedirs(datadir)

            for y in dates:
                que.put(Job(ename, y))

    for j in range(int(len(citys) / 100)):
        t = threading.Thread(target=doJob, name='Doer{}'.format(j), args=(que,))
        threads.append(t)
        t.start()
