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
from outputdata import OutputData

class DailyWeather(OutputData):
    def __init__(self, *args, **kwargs):
        super(DailyWeather, self).__init__(*args, **kwargs)
        self.dir_path = "/opt/weather"
        self.browser = "phantomjs"
        self.driver_path = r"{}/phantomjs/bin/phantomjs".format(self.dir_path)
        self.tmpurl = "http://tianqi.2345.com/wea_history/71294.htm"
        self.agent = "Mozilla/{x}.0 (Macintosh; Intel Mac OS X 10.9; rv:{x}.0) Firefox/{x}.0".format(x=random.randint(0,30))
        self.datatype = "daily"
        self.cssprov = "#selectProv > option"
        self.csscity = "#chengs_ls > option"
        self.today = datetime.datetime.now()

    def cusHeader(self, tmpurl=None):
        if tmpurl is None:
            tmpurl = self.tmpurl

        if self.browser == "phantomjs" :
            # self.driver_path = r"/Users/data/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs"
            # self.driver_path = r"{}/phantomjs/bin/phantomjs".format(self.dir_path)

            # dcap = dict(DesiredCapabilities.PHANTOMJS)
            # dcap["phantomjs.page.settings.userAgent"] = (self.agent)
            # dcap["phantomjs.page.customHeaders.Referer"] = (tmpurl)
            #self.driver.add_cookie({'Accept-Encoding':'gzip, deflate, sdch', 'User-Agent':self.agent})
            serargs = ['--load-images=no']
            driver = webdriver.PhantomJS(service_args=serargs, executable_path=self.driver_path)
            # driver = webdriver.PhantomJS(desired_capabilities=dcap, service_args=serargs, executable_path=self.driver_path)
        elif self.browser == "chrome" :
            self.driver_path = "/Users/data/Downloads/chromedriver"
            driver = webdriver.Chrome(self.driver_path)

        return driver

    def getCityData(self, city):
        i = city
        url = "http://tianqi.2345.com/wea_history/{}.htm".format(i[8])
        driver = self.cusHeader(tmpurl=url)
        data = []
        try:
            # driver.set_window_size(1920,1080)
            driver.get(url)
            res = BeautifulSoup(driver.page_source, "lxml")
            # driver.quit()
            daydata = res.select('#weather_tab > table > tbody > tr')
            for l in daydata:
                tmp = [i[8]]+[i.text.replace('℃','') for i in l.select('td')]
                checkwin = [i for i in tmp[5] if i.isdigit()]
                checkair = [i for i in tmp[6] if not i.isdigit()]
                winsep = lambda x: x.index(checkwin[0]) if len(checkwin) > 0 else len(x)
                airsep = lambda x: x.index(checkair[0]) if len(checkair) > 0 else len(x)
                updatetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                daily = [tmp[0], tmp[1][0:10], tmp[2], tmp[3], tmp[5][0:winsep(tmp[5])], tmp[5][winsep(tmp[5]):], tmp[6][0:airsep(tmp[6])], tmp[6][airsep(tmp[6]):], updatetime]
                data.append(daily)
        except Exception as e:
            # time.sleep(25)
            driver.save_screenshot('data/{}.png'.format(i[8]))
            print('[get data fail] {} => {}'.format(url, str(e)))
        finally:
            driver.quit()
        return data

    # def __repr__(self):
    #     return "<DailyWeather(url='{}')>".format(self.driver.current_url)

    def getCities(self):
        driver = self.cusHeader()
        geo = []
        try:
            driver.get(self.tmpurl)
            driver.find_element_by_css_selector("#switchHisCity").click()
            # tt = [option.get_attribute('value') for option in driver.find_elements_by_tag_name('option')]
            provs = [x for x in driver.find_elements_by_css_selector(self.cssprov)]
            for i in provs:
                print("[DW] - {} {}".format(i.text, i.get_attribute('value')))
                driver.find_element_by_css_selector("#selectProv > option[value='{}']".format(i.get_attribute('value'))).click()
                cities = [x for x in driver.find_elements_by_css_selector(self.csscity)]
                for j in cities:
                    driver.find_element_by_css_selector("#chengs_ls > option[value='{}']".format(j.get_attribute('value'))).click()
                    areas = [x for x in driver.find_elements_by_css_selector("#cityqx_ls > option")]
                    for m, k in enumerate(areas) :
                        tmp = [i.text, j.text, k.text, i.get_attribute('value'), j.get_attribute('value'), k.get_attribute('value')]
                        flattmp = [j for i in tmp for j in i.split(' ')]
                        geo.append(flattmp)
        except Exception as e:
            driver.save_screenshot('data/city{}.png'.format(""))
            print('[get data fail] => {}'.format(str(e)))
        finally:
            driver.quit()
        return geo
