import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import time
import selenium
from selenium import webdriver
from selenium.common import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

##Start the driver
driver = webdriver.Chrome()

#Get the page
driver.get("https://www.muscleandstrength.com/exercises")
driver.implicitly_wait(5)


exerciseLinks = driver.find_elements(By.CSS_SELECTOR, "div.mainpage-category-list .cell a")

exerciseUrls = []

for i in range(44):
    link = exerciseLinks[i].get_attribute("href")
    if (link not in exerciseUrls and (link != "https://www.muscleandstrength.com/exercises/palmar-fascia" and link != "https://www.muscleandstrength.com/exercises/plantar-fascia")): #Exclude these "muscle" groups
        exerciseUrls.append(link)

print(exerciseUrls)
print(len(exerciseUrls))

for exerciseUrl in exerciseUrls:
    driver.get(exerciseUrl)
    time.sleep(3)

    try:
        title = driver.find_element(By.TAG_NAME, 'h1').text
        print(f"Title of the category: {title}")

    except Exception as e:
        print(f"Error extracting data from {exerciseUrl}: {e}")

driver.close()

##
##{
##    'exercise1': {
##        type:
##        equipment:
##        primaryMuscles: []
##        secondary: []

##    }
##    'exercise2': {
##        type:
##        equipment:
##        primaryMuscles: []
##        secondary: []

##    }
        
##Sample

#driver.get("https://www.muscleandstrength.com/exercises/abs")
#cableCrunch = driver.find_element(By.XPATH, "//a[@href='/exercises/cable-crunch.html']")

#print(cableCrunch.text)

#cableCrunch.click()

#temp = driver.find_element(By.TAG_NAME, value = 'h5')

#print(temp.text)








##}


