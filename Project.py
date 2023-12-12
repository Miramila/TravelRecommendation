from flask import Flask, render_template, request
import pandas as pd
import requests
import numpy as np

app = Flask(__name__)

# Replace this with your actual data and analysis functions
# Example: Some dummy analysis function
def get_weather_data(lat, lng, date):
    try:
        url = f"https://api.weather.gov/points/{lat},{lng}"
        response = requests.get(url).json()
        new_url = response['properties']['forecast']
        new_response = requests.get(new_url).json()
        weather = new_response['properties']['periods'][date]['shortForecast']
        temperature = new_response['properties']['periods'][date]['temperature']
    except:
        weather = 'Not Found'
        temperature = -99
    return weather, temperature

def weather_data(date, state):
    print("Loading Weather Data...")
    global state_data
    state_data = data[data['State'] == state]
    state_data['Weather'] = pd.Series(dtype='object')
    state_data['Temperature'] = pd.Series(dtype='float64')
    for index in range(len(state_data)):
        print(index)
        lat = state_data.iloc[index,1]
        lng = state_data.iloc[index,2]
        state_data.iloc[index, 5], state_data.iloc[index, 6] = get_weather_data(lat, lng, date)

def category_temp(temp):
    if temp < 75:
        return 'cold'
    elif temp >= 120:
        return 'hot'
    else:
        return 'warm'

# date_data
date_data = {
    'This afternoon': 0,
    'Tonight': 1,
    'Tomorrow afternoon': 2,
    'Tomorrow night': 3,
    'Day after tomorrow afternoon': 4,
    'Day after tomorrow night': 5,
    'Three days later afternoon': 6,
    'Three days later night': 7,
    'Four days later afternoon': 8,
    'Four days later night': 9,
    'Five days later afternoon': 10,
    'Five days later night': 11,
    'Six days later afternoon': 12, 
    'Six days later night': 13
}


data = pd.read_csv("attractions_with_locations.csv")
states = data['State'].unique()
tree = {}

@app.route('/')
def travel_date():
    return render_template('travel_date.html', date_data = date_data, states=states)

@app.route('/analyze', methods=['POST'])
def analyze():
    if request.method == 'POST':
        travel_date = request.form['travel_date']
        state = request.form['state']
        date = date_data[travel_date]
        weather_data(date, state)

        state_data['Temp Category'] = state_data['Temperature'].astype(int).apply(category_temp)
        # make the tree
        for index, row in state_data.iterrows():
            weather = row['Weather']
            temp = row['Temp Category']
            attraction_name = row['Attraction Name']
        
        
            if weather not in tree:
                tree[weather] = {}
        
            if temp not in tree[weather]:
                tree[weather][temp] = []
        
            tree[weather][temp].append(attraction_name)

    return render_template('preferences.html', attraction_data=tree, df = state_data)

@app.route('/preferences', methods=['GET', 'POST'])
def preferences():
    if request.method == 'POST':
        weather_preference = request.form['weather_preference']
        temperature_preference = request.form['temperature_preference']
        # Query the dictionary
        result = tree.get(weather_preference, {}).get(temperature_preference, 'Not found')

    return render_template('result.html', result=result, df = state_data)

if __name__ == '__main__':
    app.run(debug=True)
