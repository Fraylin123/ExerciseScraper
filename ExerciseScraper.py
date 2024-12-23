import requests
from bs4 import BeautifulSoup
import pymongo
import time
import re
import selenium
from selenium import webdriver
from selenium.common import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium.webdriver.chrome.options import Options

##Options
chromeOptions = Options()
chromeOptions.add_argument("--disable-gpu")
chromeOptions.add_argument("--disable-software-rasterizer") 

chromeOptions.add_argument("--headless")
##

##Start the driver
driver = webdriver.Chrome(options=chromeOptions)

#Get the page
driver.get("https://www.muscleandstrength.com/exercises")
driver.implicitly_wait(5)


exerciseLinks = driver.find_elements(By.CSS_SELECTOR, "div.mainpage-category-list .cell a")
#print("The length is: ",len(exerciseLinks))

exerciseUrls = []

for i in range(len(exerciseLinks)):
    link = exerciseLinks[i].get_attribute("href")
    if (link not in exerciseUrls and (link != "https://www.muscleandstrength.com/exercises/palmar-fascia" and link != "https://www.muscleandstrength.com/exercises/plantar-fascia")): #Exclude these "muscle" groups
        exerciseUrls.append(link)


print(len(exerciseUrls))

data = {}


def getAttributes(aElements, exercisesNames):
    try:
        aElementsUrls = [element.get_attribute("href") for element in aElements]
        #print("Len of the exercises: ", len(aElementsUrls))
       
        global data 
        index = 0
        for elementUrl in aElementsUrls:
            driver.get(elementUrl)
            time.sleep(2)

            primaryMuscle = driver.find_element(By.CSS_SELECTOR, "div.field-item.even a").text
            otherA = driver.find_elements(By.CSS_SELECTOR, 'div.node-stats-block ul li')[1:]
            otherAValues = [attribute.text.split('\n')[1] for attribute in otherA]
            
            try:
                youtubeURL = driver.find_element(By.CSS_SELECTOR, 'div.video.responsive-embed.widescreen .video-wrap iframe').get_attribute("src")
            except NoSuchElementException:
                youtubeURL = ''
                
            if ("youtube" in youtubeURL):
                print("URL is: ", youtubeURL)
                pattern = r"https://www\.youtube\.com/embed/([^?&]+)"
                vidID = re.search(pattern,youtubeURL).group(1)
            else:
                vidID=None
            print("Current exercise: " + exercisesNames[index])
        
            data[exercisesNames[index]] = {
            "primaryMuscle":primaryMuscle,
            "type":otherAValues[0],
            "equipment":otherAValues[1],
            "level":otherAValues[4],
            "secondaryMuscles":otherAValues[5],
            "image": vidID
            }
           
            index+=1
    except Exception as e:
        print(f"The error is inside the function: {e}")


counter = 0    
for exerciseUrl in exerciseUrls: # For each subpage
    driver.get(exerciseUrl)
    time.sleep(1)

    try:
        title = driver.find_element(By.TAG_NAME, 'h1').text
       ## print(f"Title of the category: {title}")
        subpageExercises = driver.find_elements(By.CSS_SELECTOR, "div.cell.small-12.bp600-6 .node-title a")
        #print("Len of subpage: " , len(subpageExercises))
        subpageExercisesNames = [currE.text for currE in subpageExercises] ##Get all exercise names
       # print("Len of subpage names: " , len(subpageExercisesNames))
        #print(subpageExercisesNames)
        #print(data)
        getAttributes(subpageExercises, subpageExercisesNames)
        counter+=1
        if counter == 3:
            print(data)
            
            break
        

    except Exception as e:
        print(f"Error extracting data from {exerciseUrl}: {e}")

driver.close()


#client = pymongo.MongoClient("mongodb://localhost:27017/")
#testDb = client["test"]

#exercisesData = testDb["exercises"]
