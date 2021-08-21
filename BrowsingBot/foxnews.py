from selenium import webdriver
from selenium.webdriver.common.keys import Keys  ##gives access to enter and escape key for results
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
import time
import random
import numpy

keywords = ["us", "politics", "media", "opinion", "entertainment", "sports", "lifestyle"]
template = "https://www.foxnews.com/{}"

def timeout_click(element):
    while True:
        try:
            element.click()
            break
        except TimeoutException:
            continue
        except StaleElementReferenceException:
            break

def timeout_url(driver):
    try:
        driver.get("https://www.foxnews.com/")
    except TimeoutException:
        driver.execute_script("window.stop();")

def ad_popup(driver):
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "pf-widget-close"))).click()
    except:
        pass

def exception_handler(e): ##if exception, close all pages and start over
    print("\n\n----------------------------------------------------")
    print("ETSY")
    print("----------------------------------------------------")
    print(e)
    print("----------------------------------------------------")

def fox_news_run(driver):
    timeout_url(driver)

    for i in keywords:
        try:
            driver.get(template.format(i))
            time.sleep(3)
            article = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "article.story-1")))
            time.sleep(2)
            driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center'});", article)
            time.sleep(3)
            timeout_click(article)
            time.sleep(2)
            articleBody = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "article-body")))
            articleLoc = articleBody.location
            articleSize = articleBody.size
            startY = articleLoc["y"]
            height = articleSize["height"]
            driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth'});", articleBody)
            time.sleep(1)
            ad_popup(driver)
            for j in numpy.arange(startY, height, random.uniform(0.04, 0.1)):
                driver.execute_script("window.scrollTo(0, {});".format(j))
            time.sleep(3)
            currentOffset = driver.execute_script("return window.pageYOffset;")
            for k in numpy.arange(currentOffset, 0, random.uniform(-0.04, -0.1)):
                driver.execute_script("window.scrollTo(0, {});".format(k))
            time.sleep(2)
        except Exception as e:
            exception_handler(e)
            continue
