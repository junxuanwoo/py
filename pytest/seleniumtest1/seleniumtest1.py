# coding = utf-8
from selenium import webdriver
driver =webdriver.Chrome()
driver.get('http://radar.kuaibo.com')
print driver.title
driver.quit()