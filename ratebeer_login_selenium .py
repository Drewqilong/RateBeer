# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 17:38:27 2019

@author: Jerry
"""


# jdmiaosha_selenium

from selenium import webdriver
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import bs4
import time
from lxml import etree

#Wait unitl some elements appeared
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


url="https://www.ratebeer.com/brewers/avondale-brewing-company/12890/"

##Set user-agent for PhantomJS
#dcap = dict(DesiredCapabilities.PHANTOMJS)
#dcap["phantomjs.page.settings.userAgent"] = (
#    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36 "
#)
# 
#
## 使用webdriver.PhantomJS
#browser=webdriver.PhantomJS(executable_path='E:\\phantomjs-2.1.1-windows\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe', desired_capabilities=dcap)


#simulate the user open the browser to surf Internet
userProfile = "C:\\Users\\Jerry\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("user-data-dir={}".format(userProfile))
# add here any tag you want.
chrome_options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors", "safebrowsing-disable-download-protection", "safebrowsing-disable-auto-update", "disable-client-side-phishing-detection"])

# solve the WebDriverException: chrome not reachable
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-setuid-sandbox")
#chrome_options.add_argument("--remote-debugging-port=12582")
#chrome_options.add_argument("--remote-debugging-port=9222")
#chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-dev-shm-using")


browser = webdriver.Chrome(executable_path='E:\\Python\\chromedriver_win32_2.40\\chromedriver.exe', options=chrome_options)

#Get initial web page
browser.get(url)

import browser_cookie3
cookies = browser_cookie3.firefox(domain_name='.ratebeer.com')
for cj in cookies:
    cookie = cj.__dict__
    browser.add_cookie(cookie)
#browser.execute_script("arguments[0].click()",browser.find_element_by_id("ctrl_pageLogin_registered"))

#browser.find_element_by_id("ctrl_pageLogin_registered").click()
#browser.find_element_by_xpath('//button[normalize-space()="Allow All"]').click()


#browser.find_element_by_xpath("//*[@class='optanon-allow-all accept-cookies-button']").click()
browser.get(url)


#browser.find_elements_by_id('ctrl_pageLogin_login')[-1].send_keys("drewqilong@live.com")
#browser.find_elements_by_id('ctrl_pageLogin_password')[-1].send_keys("B71MzlmyB@jxT(S")
#browser.find_elements_by_xpath("//input[@type='submit' and @value='Log in']")[-1].click()
#browser.get("https://www.beeradvocate.com/community")


#WebDriverWait(browser,20).until(EC.visibility_of_element_located((By.CLASS_NAME,'seckill_container')))



# 执行js得到整个dom
html = browser.execute_script("return document.documentElement.outerHTML")

#while True:
#
#    soup = bs4.BeautifulSoup(html, 'lxml')
    
