import time
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys ##gives access to enter and escape key for results
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import numpy as np
import pyautogui
import bezier
from selenium.common.exceptions import *

def automation_alert_removal():
    options = webdriver.ChromeOptions()  # Initializing Chrome Options from the Webdriver
    options.add_experimental_option("useAutomationExtension", False)  # Adding Argument to Not Use Automation Extension
    options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Excluding enable-automation Switch

    driver = webdriver.Chrome(options=options)  # Initialzing Chromedriver and giving argument options which is initialized and modified before

# enter input one letter at a time
def slow_type(pageElem, pageInput):
    for letter in pageInput:
        time.sleep(float(random.uniform(.05, .3)))
        pageElem.send_keys(letter)


def slow_scroll_endless(driver): ##slow scroll on an endless webpage
    #get scroll height
    lastHeight = driver.execute_script("return document.body.scrollHeight")
    beginHeight = 1

    while True:
        #slow scroll to bottom
        for i in range(beginHeight, lastHeight, random.randint(3,5)):
            driver.execute_script("window.scrollTo(0, {});".format(i))
            #pretend to read
            pause = random.randint(1,1000)
            if pause == 3:
                time.sleep(5)

        #wait to load page
        time.sleep(3)

        #calculate new scroll height and compare with last scroll height
        newHeight = driver.execute_script("return document.body.scrollHeight")
        if newHeight == lastHeight:
            break
        beginHeight = lastHeight
        lastHeight = newHeight

def bezier_mouse(location, size, panelHeight): ##move mouse to middle of element
    x, relY = location["x"], location["y"]
    absY = relY + panelHeight
    w, h = size["width"], size["height"]
    wCenter = w/2
    hCenter = h/2
    xCenter = int(wCenter + x)
    yCenter = int(hCenter + absY)

    start = pyautogui.position()
    end = xCenter, yCenter

    x2 = (start[0] + end[0])/2 #midpoint x
    y2 = (start[1] + end[1]) / 2 ##midpoint y

    control1X = (start[0] + x2)/2
    control1Y = (end[1] + y2) / 2

    control2X = (end[0] + x2) / 2
    control2Y = (start[1] + y2) / 2

    # Two intermediate control points that may be adjusted to modify the curve.
    control1 = control1X, y2 ##combine midpoints to creat perfect curve
    control2 = control2X, y2


    # Format points to use with bezier
    control_points = np.array([start, control1, control2, end])
    points = np.array([control_points[:, 0], control_points[:, 1]])  # Split x and y coordinates
    # You can set the degree of the curve here, should be less than # of control points
    degree = 3
    # Create the bezier curve
    curve = bezier.Curve(points, degree)

    curve_steps = 50  # How many points the curve should be split into. Each is a separate pyautogui.moveTo() execution
    delay = 0.003  # Time between movements. 1/curve_steps = 1 second for entire curve

    # Move the mouse
    for j in range(1, curve_steps + 1):
        # The evaluate method takes a float from [0.0, 1.0] and returns the coordinates at that point in the curve
        # Another way of thinking about it is that i/steps gets the coordinates at (100*i/steps) percent into the curve
        x, y = curve.evaluate(j / curve_steps)
        pyautogui.moveTo(x, y)  # Move to point in curve
        pyautogui.sleep(delay)  # Wait delay

def mouse_after_scroll_into_view(location, size, panelHeight):
    screenWidth, screenHeight = pyautogui.size()
    centerHeight = (screenHeight - panelHeight)/2 ##bezier_mouse adds panel height so subtract for accurate y after scroll
    x = location["x"]
    w, h = size["width"], size["height"]
    wCenter = w/2
    xCenter = int(wCenter + x)
    yCenter = int(centerHeight + (panelHeight/2))

    start = pyautogui.position()
    end = xCenter, yCenter

    x2 = (start[0] + end[0])/2 #midpoint x
    y2 = (start[1] + end[1]) / 2 ##midpoint y

    control1X = (start[0] + x2)/2
    control1Y = (end[1] + y2) / 2

    control2X = (end[0] + x2) / 2
    control2Y = (start[1] + y2) / 2

    # Two intermediate control points that may be adjusted to modify the curve.
    control1 = control1X, y2 ##combine midpoints to creat perfect curve
    control2 = control2X, y2


    # Format points to use with bezier
    control_points = np.array([start, control1, control2, end])
    points = np.array([control_points[:, 0], control_points[:, 1]])  # Split x and y coordinates
    # You can set the degree of the curve here, should be less than # of control points
    degree = 3
    # Create the bezier curve
    curve = bezier.Curve(points, degree)

    curve_steps = 50  # How many points the curve should be split into. Each is a separate pyautogui.moveTo() execution
    delay = 0.003 # Time between movements. 1/curve_steps = 1 second for entire curve

    # Move the mouse
    for j in range(1, curve_steps + 1):
        # The evaluate method takes a float from [0.0, 1.0] and returns the coordinates at that point in the curve
        # Another way of thinking about it is that i/steps gets the coordinates at (100*i/steps) percent into the curve
        x, y = curve.evaluate(j / curve_steps)
        pyautogui.moveTo(x, y)  # Move to point in curve
        pyautogui.sleep(delay)  # Wait delay

def resting_mouse(): #move mouse to right of screen

    start = pyautogui.position()
    end = random.randint(1600,1750), random.randint(400,850)

    x2 = (start[0] + end[0])/2 #midpoint x
    y2 = (start[1] + end[1]) / 2 ##midpoint y

    control1X = (start[0] + x2)/2
    control2X = (end[0] + x2) / 2

    # Two intermediate control points that may be adjusted to modify the curve.
    control1 = control1X, y2 ##combine midpoints to create perfect curve
    control2 = control2X, y2 ## using y2 for both to get a more linear curve

    # Format points to use with bezier
    control_points = np.array([start, control1, control2, end])
    points = np.array([control_points[:, 0], control_points[:, 1]])  # Split x and y coordinates
    # You can set the degree of the curve here, should be less than # of control points
    degree = 3
    # Create the bezier curve
    curve = bezier.Curve(points, degree)

    curve_steps = 50  # How many points the curve should be split into. Each is a separate pyautogui.moveTo() execution
    delay = 0.003  # Time between movements. 1/curve_steps = 1 second for entire curve

    # Move the mouse
    for j in range(1, curve_steps + 1):
        # The evaluate method takes a float from [0.0, 1.0] and returns the coordinates at that point in the curve
        # Another way of thinking about it is that i/steps gets the coordinates at (100*i/steps) percent into the curve
        x, y = curve.evaluate(j / curve_steps)
        pyautogui.moveTo(x, y)  # Move to point in curve
        pyautogui.sleep(delay)  # Wait delay
    time.sleep(2)
