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

def logged_in_check(driver):
    try:
        profile = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "//div[@data-testid='topmenu-profile']")))
        driver.execute_script("arguments[0].click();", profile)
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@data-id='LOGOUT']")))
        print("WISH: sign in successful")
        return True
    except:
        return False

def wish_run(driver):
    global loginAttempts

    if loginAttempts < 4:
        try:
            username, password = login_info()
            driver.get("https://www.wish.com/?hide_login_modal=true")

            isLoggedIn = logged_in_check(driver)

            if isLoggedIn == True:
                return
            elif isLoggedIn == False:
                try:
                    emailElement = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "//input[@data-testid='login-username']")))
                    emailElement.click()
                    time.sleep(0.5)
                    emailElement.send_keys(username)
                    time.sleep(5)
                    passwordElement = driver.find_element(By.XPATH, "//input[@data-testid='login-password']")
                    passwordElement.click()
                    time.sleep(0.5)
                    passwordElement.send_keys(password)
                    time.sleep(0.5)
                    passwordElement.send_keys(Keys.RETURN)

                    isLoggedIn = logged_in_check(driver)

                    if isLoggedIn == True:
                        return
                    elif isLoggedIn == False:
                        loginAttempts += 1
                        wish_run(driver)
                except:
                    loginAttempts += 1
                    wish_run(driver)
        except:
            loginAttempts += 1
            wish_run(driver)
    else:
        print("WISH: sign in NOT successful")