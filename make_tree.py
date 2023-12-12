import pandas as pd
import numpy as np
import requests
from flask import Flask, render_template, request
import json

def get_weather_data(lat, lng, date):
    try:
        url = f"https://api.weather.gov/points/{lat},{lng}"
        response = requests.get(url).json()
        new_url = response['properties']['forecast']
        new_response = requests.get(new_url).json()
        weather = new_response['properties']['periods'][date]['shortForecast']
        temperature = new_response['properties']['periods'][date]['temperature']
        print(weather, temperature)
    except:
        weather = "Not Found"
        temperature = -99
    return weather, temperature

def category_temp(temp):
    if temp < 75:
        return 'cold'
    elif temp >= 120:
        return 'hot'
    else:
        return 'warm'


data = pd.read_csv("attractions_with_locations.csv")
data['Weather'] = pd.Series(dtype='object')
data['Temperature'] = pd.Series(dtype='float64')
date = int(input("When do you want to go: "))
for index in range(len(data)):
    lat = data.loc[index,'Latitude']
    lng = data.loc[index,'Longitude']
    data.loc[index, 'Weather'], data.loc[index, 'Temperature'] = get_weather_data(lat, lng, date)

data = pd.read_csv("attractions_with_weather_in_date1.csv")
data.dropna(inplace=True)

data['Temp Category'] = data['Temperature'].astype(int).apply(category_temp)

# make the tree

tree = {}

for index, row in data.iterrows():
    state = row['State']
    weather = row['Weather']
    temp = row['Temp Category']
    attraction_name = row['Attraction Name']

    if state not in tree:
        tree[state] = {}

    if weather not in tree[state]:
        tree[state][weather] = {}

    if temp not in tree[state][weather]:
        tree[state][weather][temp] = []

    tree[state][weather][temp].append(attraction_name)

file_path = "tree_with_states.json"
with open(file_path, 'w') as json_file:
    json.dump(tree, json_file, indent=2)






