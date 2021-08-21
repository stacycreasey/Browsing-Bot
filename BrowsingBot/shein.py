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
        username = data[0][0]
        password = data[0][1]
    return username, password

def ad_popup(driver):
    try:
        WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.CLASS_NAME, "coupon-poplayer-modal"))) ##coupon popup
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-close"))).click()
    except:
        pass

def logged_in_check(driver):
    try:
        loggedIn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "user-dropdown")))
        WebDriverWait(loggedIn, 5).until(EC.presence_of_element_located((By.XPATH, "//em[contains(text(), 'My Profile')]")))
        print("SHEIN: sign in successful")
        return True
    except:
        return False

def shein_run(driver):
    global loginAttempts

    if loginAttempts < 4:
        try:
            username, password = login_info()
            driver.get("https://us.shein.com/user/auth/login")

            isLoggedIn = logged_in_check(driver)

            if isLoggedIn == True:
                return
            elif isLoggedIn == False:
                try:
                    signInBox = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "sign-in.j-sign-in")))
                    time.sleep(2)
                    emailElement = signInBox.find_element(By.NAME, "email")
                    passwordElement = signInBox.find_element(By.NAME, "password")
                    time.sleep(1)
                    emailElement.click()
                    time.sleep(0.5)
                    emailElement.send_keys(username)
                    time.sleep(0.5)
                    passwordElement.click()
                    time.sleep(0.5)
                    passwordElement.send_keys(password, Keys.RETURN)

                    isLoggedIn = logged_in_check(driver)

                    if isLoggedIn == True:
                        return
                    elif isLoggedIn == False:
                        loginAttempts += 1
                        shein_run(driver)
                except:
                    loginAttempts += 1
                    shein_run(driver)
        except:
            loginAttempts += 1
            shein_run(driver)
    else:
        print("SHEIN: sign in NOT successful")
