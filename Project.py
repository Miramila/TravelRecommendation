import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import time
from selenium.webdriver.common.by import By

def get_attractions_name(driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    name = []
    typeName = []
    location = []
    for text in soup.find_all('div', class_ = "XfVdV o AIbhI"):
        name.append(text.text.strip())
    for text in soup.select('div.BKifx > div > div > div.biGQs._P.pZUbB.hmDzD'):
        typeName.append(text.text.strip())
    # for i in range(len(name)):
    #     location.append(get_locations(driver, i))
    df = pd.DataFrame({'name': name, 'type': typeName})
    # df = pd.DataFrame({'name': name, 'type': typeName, 'location': location})
    return df

def get_locations(driver, i):
    new_window_button = driver.find_element(By.CSS_SELECTOR, f"#lithium-root > main > div.C > div > div > div.Igubo.z > div > div:nth-child(2) > div.IyYBN._T > div.C > div > div > div:nth-child(2) > div > div.JfoTr._T > div > div > section:nth-child({i+2}) > div > div > div > div > article > div.hZuqH.y > header > div > div > div > a:nth-child(1) > h3 > div > span > div")
    new_window_button.click()
    all_window_handles = driver.window_handles
    new_window_handle = all_window_handles[-1]
    driver.switch_to.window(new_window_handle)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    location = soup.select('#tab-data-WebPresentation_PoiLocationSectionGroup > div > div > div.AcNPX.A > div.ZhNYD > div > div > div > div.MJ > button > span')[0].text.strip()
    driver.close()
    original_window_handle = all_window_handles[0]
    driver.switch_to.window(original_window_handle)
    return location
    

page_num = 10
driver = webdriver.Chrome()
url = "https://www.tripadvisor.com/Attractions-g191-Activities-oa0-United_States.html"
driver.get(url)
data = pd.DataFrame(columns=['name', 'type'])
for i in range(page_num):
    time.sleep(5)
    df = get_attractions_name(driver)
    data = pd.concat([data, df], ignore_index=True)
    driver.find_element(By.CSS_SELECTOR, "#lithium-root > main > div.C > div > div > div.Igubo.z > div > div:nth-child(2) > div.IyYBN._T > div.C > div > div > div:nth-child(2) > div > div.JfoTr._T > div > div > section:nth-child(40) > div > div:nth-child(1) > div > div.OvVFl.j > div.xkSty > div > a").click()
driver.close()
driver.quit()
data.to_csv('attractions_with.csv', index=False)

