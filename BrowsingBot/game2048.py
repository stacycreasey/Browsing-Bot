from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

gameAttempts = 0

def is_over(driver):
    try:
        gameOver = driver.find_element(By.CLASS_NAME, "game-over")
        return gameOver
    except:
        pass

def game_run(driver):
    global gameAttempts

    if gameAttempts < 4:
        try:
            driver.get('https://gabrielecirulli.github.io/2048/')

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "grid-container")))  ##wait until page loaded

            gameElem = driver.find_element(By.CLASS_NAME, "grid-container")

            directions = [Keys.UP, Keys.DOWN, Keys.RIGHT, Keys.LEFT]

            ActionChains(driver).move_to_element_with_offset(gameElem, 0, 50).perform()

            time.sleep(3)

            randomGameCount = random.randint(5,15)
            gameEnded = False #set flag if game has ended
            i = 0

            while not gameEnded:
                gameEnded = is_over(driver)
                if gameEnded:
                    i += 1
                    if i == randomGameCount:
                        time.sleep(5)
                        return
                    else:
                        gameEnded = False
                    time.sleep(3)
                    restartElem = driver.find_element(By.LINK_TEXT, "Try again")
                    restartElem.click()

                for direction in directions:
                    choice = random.choice(direction)
                    time.sleep(random.randint(2,6))
                    ActionChains(driver).send_keys(choice).perform()
        except:
            gameAttempts += 1
            game_run(driver)
    else:
        print("GAME ERROR")