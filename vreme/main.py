import requests
import random
from secretstorage import item
key = '5525d503718ad744836641febc49fbdd'
url = 'https://api.openweathermap.org/data/2.5/weather'
cities = ['Sofia', 'London', 'Tokyo', 'New York', 'Toronto', 'Moscow']
picked = random.sample(cities, 5)
temps = []

def get_weather(name):
    params = {
        'q': name,
        'appid': key,
        'units': 'metric',
        'lang': 'en'
    }
    res = requests.get(url,params=params)
    if res.status_code == 200:
        return res.json()
    else:
        print("Error for", name)
        return None
    
print('Weather for 5 cities: ')
    
for city in picked:
    data = get_weather(city)
    
    if data:
        t = data[ 'main']['temp']
        h = data['main' ]['humidity']
        d = data[ 'weather'][0]['description']
         
        print(city + ": " + d + ", " + str(t) + "°C " + str(h) + "% humidity")
        
        temps.append({'c': city,'t':t})
    if len(temps)>0:
        cold = temps[0]
        for item in temps:
            if item['t']< cold['t']:
                cold = item
                
        total = 0
        for item in temps:
            total += item['t']
            avg = total/len(temps)
            
            print()
            print("Coldest:" + cold['c']+ "("+ str(cold['t']) + "°C)")
            print("Average temp:" + str(round(avg,2)) +"°C")
    uc = input("\nEnter city:")
    ud = get_weather(uc)
    
    if ud:
        t = ud['main']['temp']
        h = ud['main']['humidity']
        d = ud['weather'][0]['description']
        
        print("Weather in "+ uc+":" +d + ","+str(t)+"°C," +str(h)+"%humidity")
        
        