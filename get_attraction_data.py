import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.by import By


def get_attractions_name(driver):
    soup = BeautifulSoup(driver.page_source, "html.parser")
    for text in soup.find_all("div", class_="XfVdV o AIbhI"):
        name = text.text.strip()
        data.loc[len(data)] = name


def get_attractions_location_types(address, geocoding_api, i):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={geocoding_api}"
    response = requests.get(url).json()
    if response['results'] == []:
        data.loc[i, "Latitude"] = np.nan
        data.loc[i, "Longitude"] = np.nan
        data.loc[i, "State"] = np.nan
        data.loc[i, "Type"] = np.nan
        return
    data.loc[i, "Latitude"] = response["results"][0]["geometry"]["location"]["lat"]
    data.loc[i, "Longitude"] = response["results"][0]["geometry"]["location"]["lng"]
    if len(response['results'][0]['address_components']) < 3:
        data.loc[i, "State"] = np.nan
    elif response['results'][0]['address_components'][-2]['types'][0] == 'administrative_area_level_1':
        data.loc[i, "State"] = response['results'][0]['address_components'][-2]['long_name']
    else:
        data.loc[i, "State"] = response['results'][0]['address_components'][-3]['long_name']
    if len(response["results"][0]["types"]) == 1:
        data.loc[i, "Type"] = response["results"][0]["types"][0]
    else:
        data.loc[i, "Type"] = response["results"][0]["types"][1]

# get attraction names
data = pd.DataFrame(columns = ['Attraction Name'])
page_num = 15
driver = webdriver.Chrome()
url = "https://www.tripadvisor.com/Attractions-g191-Activities-oa0-United_States.html"
driver.get(url)
for i in range(page_num):
    time.sleep(5)
    get_attractions_name(driver)
    driver.find_element(By.CSS_SELECTOR, "#lithium-root > main > div.C > div > div > div.Igubo.z > div > div:nth-child(2) > div.IyYBN._T > div.C > div > div > div:nth-child(2) > div > div.JfoTr._T > div > div > section:nth-child(40) > div > div:nth-child(1) > div > div.OvVFl.j > div.xkSty > div > a").click()
driver.close()
# data.to_csv('attractions.csv', index = False)

# delete useful index from attractions
# data = pd.read_csv('attractions.csv')
data['Attraction Name'] = data['Attraction Name'].str.split('\. ').str[1]
data.to_csv('attractions.csv', index = False)

# find locations of each attraction and store in csv file
geocoding_api = "AIzaSyAb1Zw0zpiOp8sol3eXo-ODpgBxf6UXDS8"
data = pd.read_csv("attractions.csv")
data['Latitude'] = pd.Series(dtype='float64')
data['Longitude'] = pd.Series(dtype='float64')
data['State'] = pd.Series(dtype='object')
data['Type'] = pd.Series(dtype='object')
for i in range(len(data)):
    address = data.loc[i, "Attraction Name"].replace(" ", "+")
    print(address)
    get_attractions_location_types(address, geocoding_api, i)
data = data.dropna()
data.to_csv('attractions_with_locations.csv', index = False)
