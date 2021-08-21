from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys  ##gives access to enter and escape key for results
import time

loginAttempts = 0

def login_info():
    with open("usernamesPasswords.txt", "r") as infile:
        data = [line.rstrip().split(":") for line in infile]
        username = data[1][0]
        password = data[1][1]
    return username, password

def ad_popup(driver):
    try:
        WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.CLASS_NAME, "layui-layer1"))) ##popup
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "layui-layer-ico.layui-layer-close.layui-layer-close2"))).click()
    except:
        pass

def logged_in_check(username, driver):
    try:
        signInButton = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "headUser_name.js-labelUserName")))
        signInButton.find_element(By.XPATH, "//a[contains(text(), '" + username + "')]")
        print("GEARBEST: sign in successful")
        return True
    except:
        return False

def gearbest_run(driver):
    global loginAttempts

    if loginAttempts < 4:
        try:
            username, password = login_info()
            driver.get("https://www.gearbest.com/")
            ad_popup(driver)

            isLoggedIn = logged_in_check(username,driver)

            if isLoggedIn == True:
                return
            elif isLoggedIn == False:
                try:
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "js-panelUserInfo"))).click() ##drop down menu
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "headUser_btnLogin"))).click() ##sign in button
                    emailElement = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "email")))
                    emailElement.send_keys(username)
                    passwordElement = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "password")))
                    passwordElement.send_keys(password, Keys.RETURN)

                    isLoggedIn = logged_in_check(username, driver)

                    if isLoggedIn == True:
                        return
                    elif isLoggedIn == False:
                        loginAttempts += 1
                        gearbest_run(driver)
                except:
                    loginAttempts += 1
                    gearbest_run(driver)
        except:
            loginAttempts += 1
            gearbest_run(driver)
    else:
        print("GEARBEST: sign in NOT successful")
