
# coding: utf-8

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

outfile = open('touzhongwang.csv', 'w')


#deal with invidual event tag
def unit(tag):
    expand_nob = tag.find_element_by_xpath(".//div[6]")
    expand_nob.click()
    date = tag.find_element_by_xpath(".//div[1]").text.encode('utf-8')
    title = tag.find_element_by_xpath(".//div[2]").text.encode('utf-8')
    financier = tag.find_element_by_xpath(".//div[8]/div[5]/div[2]/a").text.encode('utf-8')
    quantity = tag.find_element_by_xpath(".//div[4]/div[1]").text.encode('utf-8')
    rounds = tag.find_element_by_xpath(".//div[4]/div[2]/span").text.encode('utf-8')
    product = tag.find_element_by_xpath(".//div[8]/div[1]/div[2]").text.encode('utf-8')
    stock = tag.find_element_by_xpath(".//div[8]/div[3]/div[2]").text.encode('utf-8')
    industry = tag.find_element_by_xpath(".//div[8]/div[2]/div[2]").text.encode('utf-8')
    value = tag.find_element_by_xpath(".//div[8]/div[4]/div[2]").text.encode('utf-8')
    register = tag.find_element_by_xpath(".//div[8]/div[6]/div[2]").text.encode('utf-8')
    investor_block = tag.find_element_by_xpath(".//div[8]/div[7]/div[2]").find_elements(By.XPATH, ".//a")
    investors = ""
    for n, i in enumerate(investor_block):
        if n == 0:
            investors += i.text.encode('utf-8')
        elif n > 0:
            investors += ';' + i.text.encode('utf-8')
    result = pd.DataFrame({'date': [date], 'title': [title], 'financier': [financier], 'quantity': [quantity], 'rounds': [rounds],
           'product': [product], 'stock': [stock], 'industry': [industry], 'value': [value], 'register': [register],
           'investors': [investors]})
    return result


#main flow
url = 'https://www.chinaventure.com.cn/event/list.shtml'
username = 'skatekang@126.com'
password = 'I8840N82Jtouzhong'
driver = webdriver.Firefox()
driver.set_window_size(1000, 1000)
driver.get(url)
wait = WebDriverWait(driver, 10)
time.sleep(2)
element = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[1]/a[2]")
element.click()
element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='loginName']")))
element.send_keys(username)
element = driver.find_element_by_xpath("//*[@id='pwd']")
element.send_keys(password + Keys.ENTER)
time.sleep(2)
element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='investEventList']")))
EVENT_LIST = driver.find_elements(By.XPATH, "//*[@id='investEventList']/li")
more_knob = driver.find_elements(By.XPATH, "//*[@id='investLoadMore']/a")
while len(more_knob) == 0:
    print 'No more knob'
    EVENT_LIST[-1].location_once_scrolled_into_view
    time.sleep(3)
    more_knob = driver.find_elements(By.XPATH, "//*[@id='investLoadMore']/a")
cnt = 0
while True:
    element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='investEventList']")))
    EVENT_LIST = driver.find_elements(By.XPATH, "//*[@id='investEventList']/li")
    while len(EVENT_LIST) == cnt:
        time.sleep(0.5)
        EVENT_LIST = driver.find_elements(By.XPATH, "//*[@id='investEventList']/li")
    DATA = pd.DataFrame({'date': [], 'title': [], 'financier': [], 'quantity': [], 'rounds': [], 'product': [],
                        'stock': [], 'industry': [], 'value': [], 'register': [], 'investors': []})
    for n, li in enumerate(EVENT_LIST):
        if n <= cnt:
            continue
        try:
            DATA = pd.concat([DATA, unit(li)])
        except Exception as e:
            print e
    DATA.to_csv(outfile)
    cnt = len(EVENT_LIST)
    more_knob = driver.find_element_by_xpath("//*[@id='investLoadMore']/a")
    more_knob.click()
driver.quit()
outfile.close()

