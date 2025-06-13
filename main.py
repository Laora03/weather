from flask import Flask, render_template, request, redirect, url_for
import requests
import random
import re

app = Flask(__name__)


API_KEY = '5525d503718ad744836641febc49fbdd'
WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather'
CITY_LIST_URL = "https://raw.githubusercontent.com/lutangar/cities.json/master/cities.json"


def get_real_cities():
    try:
        res = requests.get(CITY_LIST_URL)
        if res.status_code == 200:
            data = res.json()
            return [city['name'] for city in data]
    except:
        return []
    return []


def clean_city_name(name):
    return re.sub(r"\s*.*?", "", name).strip()


def get_weather(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric',
        'lang': 'en'
    }
    res = requests.get(WEATHER_URL, params=params)
    if res.status_code == 200:
        data = res.json()
        return {
            'city': city,
            'description': data['weather'][0]['description'],
            'temp': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'icon': data['weather'][0]['icon']
        }
    return None


@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    error = None
    random_weather = []
    temps = []
    coldest = None
    average_temp = None

   
    cities = get_real_cities()
    if len(cities) >= 5:
        picked = random.sample(cities, 5)
        for city in picked:
            cleaned = clean_city_name(city)
            data = get_weather(cleaned)
            if data:
                random_weather.append(data)
                temps.append(data['temp'])
                if not coldest or data['temp'] < coldest['temp']:
                    coldest = data
        if temps:
            average_temp = round(sum(temps) / len(temps), 2)
    else:
        error = "Not enough valid cities found."

   
    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            weather_data = get_weather(clean_city_name(city))
            if not weather_data:
                error = f"City '{city}' not found!"

    return render_template('index.html',
                           weather=weather_data,
                           error=error,
                           random_weather=random_weather,
                           coldest=coldest,
                           average_temp=average_temp)


@app.route('/refresh')
def refresh():
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=5001)