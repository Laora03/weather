# Import Module
from tkinter import *
import requests
import random
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
    

        
# create root window
root = Tk()

# root window title and dimension
root.title("Weather")
# Set geometry(widthxheight)
root.geometry('350x200')

# adding menu bar in root window
# new item in menu bar labelled as 'New'
# adding more items in the menu bar 
menu = Menu(root)
item = Menu(menu)
item.add_command(label='New')
menu.add_cascade(label='File', menu=item)
root.config(menu=menu)

# adding a label to the root window
lbl = Label(root, text = "What is the weather in ")
lbl.grid()

# adding Entry Field
txt = Entry(root, width=10)
txt.grid(column =1, row =0)


# function to display user text when
# button is clicked
def clicked():
    city = txt.get()
    data = get_weather(city)
    
    if data:
        t = data['main']['temp']
        h = data['main']['humidity']
        d = data['weather'][0]['description']
        res = city + ": " + d + ", " + str(t) + "°C, " + str(h) + "% humidity"
    else:
        res = "Error: the city '" + city + "' was not found."
    
    lbl.configure(text=res)

# button widget with red color text inside
btn = Button(root, text = "Click me" ,
             fg = "red", command=clicked)
# Set Button Grid
btn.grid(column=2, row=0)

# Execute Tkinter
root.mainloop()

   
    