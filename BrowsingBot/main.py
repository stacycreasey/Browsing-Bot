import numpy
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import *
import time
import random
import datetime
from amazon import amazon_run
from foxnews import fox_news_run
from etsy import etsy_run
from aliExpress import ali_express_run
from gearbest import gearbest_run
from wish import wish_run
from shein import shein_run
from game2048 import game_run
from ebay import ebay_run
from cookieClicker import cookie_run

functionList = [amazon_run, etsy_run, fox_news_run, game_run, cookie_run, ebay_run]
loginList = [gearbest_run, ali_express_run, wish_run, shein_run]

def setDriver():
    PATH = Service("/path/to/driver")  ##constant file path of Chrome driver

    options = webdriver.ChromeOptions()  # Initializing Chrome Options from the Webdriver
    prefs = {"profile.password_manager_enabled": False, "credentials_enable_service": False, "useAutomationExtension": False}
    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option("useAutomationExtension", False)  # Adding Argument to Not Use Automation Extension
    options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Excluding enable-automation Switch
    options.add_argument("start-fullscreen")
    options.add_argument("disable-popup-blocking")
    options.add_argument("disable-notifications")
    options.add_argument("disable-gpu")  ##renderer timeout

    driver = webdriver.Chrome(options=options, service=PATH)
    driver.set_page_load_timeout(10)

    return driver

def main():
    start = datetime.datetime.now()
    random.shuffle(functionList) ##shuffles list of functions
    driver = setDriver()
    driver.get("https://www.google.com")

    for i in range(len(loginList)): ##go through login functions
        loginList[i](driver)
        time.sleep(2)
    for i in range(len(functionList)): ##go through functions in shuffled order
        functionList[i](driver)
        time.sleep(2)

    end = datetime.datetime.now()
    executionTime = end - start

    print("Start time - " + str(start))
    print("End time - " + str(end))
    print("Execution Time - " + str(executionTime))

main()