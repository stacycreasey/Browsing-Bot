from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

def cookie_run(driver):
    driver.get("http://orteil.dashnet.org/experiments/cookie/")
    time.sleep(5)
    cookie = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "cookie")))

    timeout = time.time() + 5
    game_time = time.time() * 60  # * 30 minutes

    while True:
        sleep = random.uniform(0.1, 0.4)
        time.sleep(sleep)
        cookie.click()

        if time.time() > timeout:
            current_money = int("".join(driver.find_element(By.ID, "money").text.split(",")))
            access = driver.find_elements(By.CSS_SELECTOR, "#store b")
            upgrades = [
                {"id": f"buy{i.text.split('-')[0].strip()}", "price": int("".join(i.text.split("-")[1].strip().split(",")))}
                for i in access[:-1]
            ]

            for item in upgrades[::-1]:
                if item["price"] < current_money:
                    buy = driver.find_element(By.ID, item["id"])
                    time.sleep(2)
                    buy.click()
                    break

            timeout = time.time() + 5

        if time.time() > game_time:
            time.sleep(5)
            break