# ##PROGRAMMER:STACY CREASEY
# ##DATE: 6/15/2021
# ##PROJECT: Human Activity Web Bot
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  ##gives access to enter and escape key for results
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
import time
from functions import *
import random
import pyautogui

PATH = Service("/Users/stacycreasey/Documents/chromedriver")  ##constant file path of Chrome driver

# visibleMouse = open('mouse.js').read()

options = webdriver.ChromeOptions()  # Initializing Chrome Options from the Webdriver
options.add_experimental_option("useAutomationExtension", False)  # Adding Argument to Not Use Automation Extension
options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Excluding enable-automation Switch
options.add_argument("--mute-audio")
options.add_argument("--start-fullscreen")
options.add_argument("--disable-gpu") ##renderer timeout

driver = webdriver.Chrome(options=options, service=PATH)  # Initialzing Chromedriver and giving argument options which is initialized and modified before
driver.set_page_load_timeout(10)

# Disable pyautogui pauses
pyautogui.MINIMUM_DURATION = 0
pyautogui.MINIMUM_SLEEP = 0
pyautogui.PAUSE = 0

try:
    driver.get("https://www.foxnews.com/")
except TimeoutException:
    driver.execute_script("window.stop();")

# action = ActionChains(driver)

time.sleep(3)
menuTitles = driver.find_element(By.ID, "main-nav") ##name for nav menu
aElement = menuTitles.find_elements(By.TAG_NAME, "a") ##get element with href in it
aElement.pop()
links = [x.get_attribute("href") for x in aElement]  ##pull links for menu options
# driver.execute_script(visibleMouse)
panelHeight = driver.execute_script('return window.outerHeight - window.innerHeight;')
# lol = pyautogui.position()
# print(lol)

for i in aElement:
    parentWindow = driver.window_handles[0]
    location = i.location
    size = i.size
    time.sleep(3)
    bezier_mouse(location, size, panelHeight)
    time.sleep(2)
    pyautogui.click(button="right")
    time.sleep(1)
    pyautogui.press("down") ##select new tab
    pyautogui.press("enter") ##and hit enter
    time.sleep(2)
    childWindow = driver.window_handles[1]  ##selected menu item window
    time.sleep(1)
    driver.switch_to.window(childWindow)  ##without switch stays on parent (home) window
    time.sleep(4)
    article = driver.find_element_by_class_name("article.story-1")
    driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center'});", article)
    time.sleep(1)
    mouse_after_scroll_into_view(article.location, article.size, panelHeight)
    time.sleep(3)
    article.click()
    timeout_exception(driver)
    time.sleep(2)
    article = driver.find_elements_by_tag_name("p")
    article.pop() ## pop copyright p tag
    resting_mouse()
    for j in article:
        pyautogui.moveRel(random.randint(-3, 2), random.randint(-2, 3))  ##mouse jitter on scroll
        driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center'});", j)
        time.sleep(0.3)
    driver.close()  ##closes child (product) window
    driver.switch_to.window(parentWindow)  ##switch back to parent window
    time.sleep(2)