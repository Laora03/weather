from django.shortcuts import render
from .models import WeatherEntry
import requests
import random
import re

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

def weather_view(request):
    weather_data = None
    error = None
    random_weather = []
    temps = []
    coldest = None
    average_temp = None

    cities = get_real_cities()
    if cities:
        random.shuffle(cities)
        for city in cities:
            if len(random_weather) == 5:
                break
            cleaned = clean_city_name(city)
            data = get_weather(cleaned)
            if data:
                random_weather.append(data)
                temps.append(data['temp'])
                WeatherEntry.objects.create(
                    city=data['city'],
                    description=data['description'],
                    temperature=data['temp'],
                    humidity=data['humidity'],
                    icon=data['icon']
                )
                if not coldest or data['temp'] < coldest['temp']:
                    coldest = data
        if len(random_weather) == 5:
            average_temp = round(sum(temps) / len(temps), 2)
        else:
            error = "Could not find weather for 5 cities. Try refreshing."
        
           
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
        city = request.POST.get('city')
        if city:
            weather_data = get_weather(clean_city_name(city))
            if not weather_data:
                error = f"City '{city}' not found!"
                recent_records = []

    if request.method == 'POST':
        city = request.POST.get('city')
    if city:
        weather_data = get_weather(city)
        if weather_data:
            WeatherEntry.objects.create(
                city=weather_data['city'],
                description=weather_data['description'],
                temperature=weather_data['temp'],
                humidity=weather_data['humidity'],
                icon=weather_data['icon']
            )
           
            recent_records = WeatherEntry.objects.filter(
                city__iexact=weather_data['city']
            ).order_by('-timestamp')[:10]
        else:
            error = f"City '{city}' not found!"

    return render(request, 'weather/index.html', {
        'weather': weather_data,
        'error': error,
        'random_weather': random_weather,
        'coldest': coldest,
        'average_temp': average_temp,
        'recent_records': recent_records,
    })