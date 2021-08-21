from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
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
        WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.CLASS_NAME, "coupon-poplayer-modal"))) ##coupon popup
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-close"))).click()
    except:
        pass

def logged_in_check(driver):
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "nav-user-account"))).click()  ##drop down menu
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//b[@class='welcome-name']")))
        print("ALIEXPRESS: sign in successful")
        return True
    except:
        return False

def ali_express_run(driver):
    global loginAttempts

    if loginAttempts < 4:
        try:
            username, password = login_info()
            driver.get("https://www.aliexpress.com/")
            ad_popup(driver)

            isLoggedIn = logged_in_check(driver)

            if isLoggedIn == True:
                return
            elif isLoggedIn == False:
                try:
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "nav-user-account"))).click() ##drop down menu
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "sign-btn"))).click() ##sign in button
                    emailElement = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "fm-login-id")))
                    emailElement.click()
                    time.sleep(1)
                    emailElement.send_keys(username)
                    time.sleep(1)
                    passwordElement = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "fm-login-password")))
                    passwordElement.click()
                    time.sleep(1)
                    passwordElement.send_keys(password)
                    time.sleep(1)
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "fm-button"))).click()  ##submit

                    isLoggedIn = logged_in_check(driver)

                    if isLoggedIn == True:
                        return
                    elif isLoggedIn == False:
                        loginAttempts += 1
                        ali_express_run(driver)
                except:
                    loginAttempts += 1
                    ali_express_run(driver)
        except:
            loginAttempts += 1
            ali_express_run(driver)
    else:
        print("ALIEXPRESS: sign in NOT successful")