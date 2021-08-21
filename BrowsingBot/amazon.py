import numpy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  ##gives access to enter and escape key for results
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import *
import time
import random

def get_keywords():
    keywords = []

    with open("keywordsAmazon.txt", "r") as tf:
        lines = tf.read().splitlines()  ##pull keyword searches from text and split on new line

    for line in lines:  ##add keywords to list
        keywords.append(line)

    return keywords


def link_product(tempList, driver):  ##product links for opening in new tab
    resultList = driver.find_elements(By.CLASS_NAME, "a-link-normal.a-text-normal")  ##class name for search results
    links = [x.get_attribute("href") for x in resultList]  ##pull links for search results to open product page

    for m in links:  ##removing duplicates links bc class name is broad and has multiple instances of same href
        if m not in tempList:
            tempList.append(m)

    links = tempList

    return links


def product_page(driver):  ##coords and dimensions to scroll through page
    reviews = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "reviewsMedley")))
    height = reviews.size["height"]
    location = reviews.location["y"]
    endCoord = height + location

    return endCoord

def next_page(keyword):
    template = "https://www.amazon.com/s?k={}"
    keyword = keyword.replace(" ", "+")

    url = template.format(keyword)
    url += "&page={}"

    return url

def exception_handler(e, driver): ##if exception, close all pages and start over
    print("\n\n----------------------------------------------------")
    print("AMAZON")
    print("----------------------------------------------------")
    print(e)
    print("----------------------------------------------------")
    handles = driver.window_handles
    size = len(handles)
    for x in range(1, size):
        driver.switch_to.window(handles[x])
        driver.close()
    driver.switch_to.window(handles[0])

def random_step_creator(intervalStart, intervalStop, minValue = 0.05, maxValue = 1.5):
   randomList = [intervalStart]
   numvalue = intervalStart
   while (numvalue < intervalStop):
       numvalue += minValue + random.uniform(0,(maxValue-minValue))
       randomList.append(numvalue)
   return randomList

def slow_type(pageElem, pageInput):
    time.sleep(2)
    for letter in pageInput:
        time.sleep(float(random.uniform(.05, .3)))
        pageElem.send_keys(letter)

def amazon_run(driver):
    numKeywords = random.randint(15,25)
    numPages = random.randint(7,20)
    driver.get("https://www.amazon.com/")
    for i in range(numKeywords):
        keyword = random.choice(get_keywords())
        search = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "twotabsearchtextbox")))
        time.sleep(2)
        slow_type(search, keyword)
        url = next_page(keyword)
        try:
            for j in range(1,numPages): ## 21 = 20 pages for amazon, adjust to needs
                tempList = []
                time.sleep(2)
                driver.get(url.format(j))
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "a-link-normal.a-text-normal")))
                links = link_product(tempList, driver)

                for k in range(0, len(links)):
                    parentWindow = driver.window_handles[0]
                    fullLink = links[k]  ##starts at index 0
                    partialLink = fullLink.removeprefix("https://www.amazon.com")  ##href doesnt use this prefix but web element did
                    elementLink = driver.find_element(By.XPATH, '//a[contains(@href, "' + partialLink + '")]')

                    middleElemY = (elementLink.size['height'] / 2) + elementLink.location['y']
                    currentY = driver.execute_script("return window.innerHeight") / 2
                    middleWindowY = middleElemY - currentY
                    yOffset = driver.execute_script("return window.pageYOffset")

                    scrollBreakpoint = random.randint(600,800) ## number of pixels for scroll pause

                    randomList = random_step_creator(yOffset, middleWindowY) ##changing step count with each scroll

                    time.sleep(2)
                    for l in randomList:
                        driver.execute_script("window.scrollTo(0, {});".format(l))
                        if l >= scrollBreakpoint:  ##pause after number of pixels scrolled
                            sleep = random.uniform(0.2,1)
                            time.sleep(sleep)
                            scrollBreakpoint += random.randint(600,800)
                        else:
                            pass

                    time.sleep(4)
                    driver.execute_script("window.open('" + fullLink + "')")  ##open product in new tab
                    time.sleep(5)
                    childWindow = driver.window_handles[1]  ##product window
                    time.sleep(3)
                    driver.switch_to.window(childWindow)  ##without switch stays on parent (home) window
                    time.sleep(1)

                    endCoord = product_page(driver)

                    randomListProduct = random_step_creator(0, endCoord)  ##changing step count with each scroll
                    scrollBreakpointProduct = random.randint(600,800)
                    for m in randomListProduct:
                        driver.execute_script("window.scrollTo(0, {});".format(m))
                        if m >= scrollBreakpointProduct:  ##pause after number of pixels scrolled
                            sleep = random.uniform(0.2,3)
                            time.sleep(sleep)
                            scrollBreakpointProduct += random.randint(600,800)
                        else:
                            pass
                    time.sleep(3)
                    driver.close()  ##closes child (product) window
                    driver.switch_to.window(parentWindow)  ##switch back to parent window
        except Exception as e:
            exception_handler(e, driver)
