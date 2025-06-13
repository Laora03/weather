import requests
import random


key = '5525d503718ad744836641febc49fbdd'
url = 'https://api.openweathermap.org/data/2.5/weather'
temps = []


def get_city_list():
    response = requests.get("https://countriesnow.space/api/v0.1/countries/population/cities")
    if response.status_code == 200:
        data = response.json()
        cities = [item['city'] for item in data['data']]
        return cities
    else:
        return []


def get_weather(name):
    params = {
        'q': name,
        'appid': key,
        'units': 'metric',
        'lang': 'en'
    }
    res = requests.get(url, params=params)
    if res.status_code == 200:
        return res.json()
   


def get_valid_cities(all_cities):
    valid = []
    for city in all_cities:
        if get_weather(city):
            valid.append(city)
        if len(valid) >= 10:  
            break
    return valid


cities = get_city_list()
valid_cities = get_valid_cities(cities)

if len(valid_cities) < 5:
    print("Not enough valid cities found.")
    exit()

picked = random.sample(valid_cities, 5)
print("\nWeather for 5 cities:\n")

for city in picked:
    data = get_weather(city)
    if data:
        t = data['main']['temp']
        h = data['main']['humidity']
        d = data['weather'][0]['description']
        print(city + ": " + d + ", " + str(t) + "°C, " + str(h) + "% humidity")
        temps.append({'c': city, 't': t})


if temps:
    cold = min(temps, key=lambda x: x['t'])
    avg = sum(item['t'] for item in temps) / len(temps)

    print()
    print("Coldest: " + cold['c'] + " (" + str(cold['t']) + "°C)")
    print("Average temp: " + str(round(avg, 2)) + "°C")

uc = input("\nEnter a city to check weather: ")
ud = get_weather(uc)

if ud:
    t = ud['main']['temp']
    h = ud['main']['humidity']
    d = ud['weather'][0]['description']
    print("Weather in " + uc + ": " + d + ", " + str(t) + "°C, " + str(h) + "% humidity")
else:
    print("Error: the city '" + uc + "' was not found.")
    
    
    
    
    