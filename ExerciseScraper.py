import requests
from bs4 import BeautifulSoup
import pymongo
import time
import re
import pandas as pd

data = {}

def getPage(url):
    base_url = "https://www.muscleandstrength.com"
    if not url.startswith("http"):
        url = f"{base_url}{url}"

    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.text

#Scrapes individual exercises from each muscle category
def individualExercise(url):
    html = getPage(url)
    soup = BeautifulSoup(html, "html.parser")
    try:
        primaryMuscle = soup.select_one("div.field-item.even a").text.strip()
        otherA = soup.select("div.node-stats-block ul li")[1:]
        print(otherA[1].text)
        print(otherA[2].text)
        print(otherA[3].text)

        print("exiting")
        exit()
        otherAValues = [attribute.text.split("\n")[1] for attribute in otherA]
        
        youtubeURL = None
        youtubeElement = soup.select_one("div.video.responsive-embed.widescreen .video-wrap iframe")

        if youtubeElement:
            youtubeURL = youtubeElement.get("src", "")
            if "youtube" in youtubeURL:
                pattern =  r"https://www\.youtube\.com/embed/([^?&]+)"
                vidID = re.search(pattern, youtubeURL).group(1)
            else:
                vidID = None
        
        return {
            "primaryMuscle":primaryMuscle,
            "type":otherAValues[0],
            "equipment":otherAValues[1],
            "level":otherAValues[4],
            "secondaryMuscles":otherAValues[5],
            "image": vidID
        }
    
    except Exception as e:
        print(f"Failed to parse this page ({url}): {e}")


def getCategory(url):
    page = 1
    index = 0
    while True:
        print(f"Scraping page {page}: {url}")
        html = getPage(url)
        soup = BeautifulSoup(html, "html.parser")
        exercises = soup.select("div.cell.small-12.bp600-6 .node-title a")
        exercisesNames = [currE.text for currE in exercises]
        exercisesUrls = [exercise.get("href") for exercise in exercises]

        for exerciseUrl in exercisesUrls:
            exerciseData = individualExercise(exerciseUrl)
            if exerciseData:
                data[exercisesNames[index]] = exerciseData
        
        print(data)

        nextButton = soup.select_one(".pager-next a")
        if nextButton:
            url = nextButton.get("href")
            page+=1
            time.sleep(1)
        else:
            break



soup = BeautifulSoup(getPage("https://www.muscleandstrength.com/exercises"), "html.parser")


#Exercise categories links
#exerciseLinks = driver.find_elements(By.CSS_SELECTOR, "div.mainpage-category-list .cell a")
ecLinks = soup.select("div.mainpage-category-list .cell a")

ecUrls = []

for i in range(len(ecLinks)):
    link = ecLinks[i].get("href")
    if (link not in ecUrls and (link != "https://www.muscleandstrength.com/exercises/palmar-fascia" and link != "https://www.muscleandstrength.com/exercises/plantar-fascia")): #Exclude these "muscle" groups
        ecUrls.append(link)

ecUrls = ecUrls[:22]


for link in ecUrls:
    print(link)
    getCategory(link)

        
print("Scraping complete")


#client = pymongo.MongoClient("mongodb://localhost:27017/")
#testDb = client["test"]

#exercisesData = testDb["exercises"]