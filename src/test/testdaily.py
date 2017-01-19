#!/usr/bin/env python
#-*- coding: utf-8 -*-
import unittest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.select import Select
from daily import DailyWeather
from bs4 import BeautifulSoup

class TestDL(unittest.TestCase):
    def setUp(self):
        self.DL = DailyWeather()
        self.DL.cusHeader()
        self.driver = self.DL.driver
        self.url = "http://tianqi.2345.com/wea_history/71294.htm" # self.DL.url
        # self.driver.set_window_size(1120, 550)
        print("[url] - {} ".format(self.url))

    def test_header(self):
        cap_dict = self.driver.desired_capabilities
        for key in cap_dict:
            print("[header] - {}: {}".format(key, cap_dict[key]))

    def test_url(self):
        i = ['X', '香港', 'X', '香港', 'X', '香港', '39', '39,0', '45007']
        self.driver.get(self.url)
        self.driver.find_element_by_css_selector("#switchHisCity").click()
        self.DL.cusHeader()
        self.driver.find_element_by_css_selector("#selectProv > option[value='{}']".format(i[6])).click()
        self.driver.find_element_by_css_selector("#chengs_ls > option[value='{}']".format(i[7])).click()
        self.driver.find_element_by_css_selector("#cityqx_ls > option[value='{}']".format(i[8])).click()
        self.driver.find_element_by_css_selector('#buttonsdm_dz').click() # rerenden page
        print(self.driver.desired_capabilities)
        # self.DL.cusHeader()
        # res = BeautifulSoup(self.driver.page_source, "lxml")
        # data = res.select('#weather_tab > table > tbody > tr')
        # print(data)
        # self.driver.find_element_by_id(
        #     'search_form_input_homepage').send_keys("realpython")
        # self.driver.find_element_by_id("search_button_homepage").click()
        # self.assertIn(
        #     "https://duckduckgo.com/?q=realpython", self.driver.current_url
        # )

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()
    #print(DL)
