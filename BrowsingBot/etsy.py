import numpy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  ##gives access to enter and escape key for results
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import *
from selenium.webdriver import ActionChains
import time
import random


def get_keywords(): ##search term
    keywords = []

    with open("keywordsEtsy.txt", "r") as tf:
        lines = tf.read().splitlines()  ##pull keyword searches from text and split on new line

    for line in lines:  ##add keywords to list
        keywords.append(line)

    return keywords

def link_product(tempList, driver): ##product links for opening in new tab
    resultList = driver.find_element(By.CLASS_NAME, "wt-grid.wt-grid--block.wt-pl-xs-0.tab-reorder-container")  ##class name for search results
    aElement = resultList.find_elements(By.TAG_NAME, "a")  ##get element with href in it
    links = [x.get_attribute("href") for x in aElement]  ##pull links for search results to open product page

    return links, aElement


def product_page(driver): ##coords and dimensions to scroll through page
    container = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "content")))
    containerLoc = container.location
    containerSize = container.size
    startY = containerLoc["y"]
    height = containerSize["height"]

    return startY, height


def next_page(keyword):
    template = "https://www.etsy.com/search?q={}"
    keyword = keyword.replace(" ", "+")

    url = template.format(keyword)
    url += "&page={}"

    return url


def exception_handler(e, driver): ##if exception, close all pages and start over
    print("\n\n----------------------------------------------------")
    print("ETSY")
    print("----------------------------------------------------")
    print(e)
    print("----------------------------------------------------")
    handles = driver.window_handles
    size = len(handles)
    for x in range(1, size):
        driver.switch_to.window(handles[x])
        driver.close()
    driver.switch_to.window(handles[0])


def etsy_run(driver):
    numKeywords = random.randint(15,25)
    numPages = random.randint(7,20)
    driver.get("https://www.etsy.com/")
    for i in range(numKeywords):
        keyword = random.choice(get_keywords())
        url = next_page(keyword)
        try:
            for j in range(1,numPages):
                driver.get(url.format(j))
                time.sleep(1)
                links, aElement = link_product(driver)
                for k in range(0, len(links)):
                    parentWindow = driver.window_handles[0]
                    time.sleep(1)
                    link = links[k]  ##start at index 0
                    element = aElement[k]
                    driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center'});", element)
                    time.sleep(3)
                    driver.execute_script("window.open('" + link + "')")  ##open product in new tab
                    childWindow = driver.window_handles[1]  ##product window
                    time.sleep(1)
                    driver.switch_to.window(childWindow)  ##without switch stays on parent (home) window
                    startY, height = product_page(driver)
                    time.sleep(1)
                    for l in numpy.arange(startY, height, random.uniform(0.04, 0.1)):
                        driver.execute_script("window.scrollTo(0, {});".format(l))
                    time.sleep(1)
                    driver.close()  ##closes child (product) window
                    driver.switch_to.window(parentWindow)  ##switch back to parent window
        except Exception as e:
            exception_handler(e, driver)