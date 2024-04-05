import tkinter as tk
import requests
import json

# Replace with your OpenWeatherMap API key
API_KEY = "8c54ddf6c115f5d6317bb97ec4093e77"

# Function to fetch weather data from OpenWeatherMap API
def get_weather(city):
    api_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    response = requests.get(api_url)
    data = json.loads(response.text)

    if response.status_code == 200 and data.get("name"):
        city_name = data["name"]
        weather = data["weather"][0]["description"]
        temperature = round(data["main"]["temp"] - 273.15, 2)
        return city_name, weather, f"{temperature}°C"
    else:
        return "Error: Could not retrieve weather data."

# Function to display weather data
def display_weather():
    city = city_entry.get()
    weather_data = get_weather(city)

    if isinstance(weather_data, tuple):
        city_name, weather, temp = weather_data
        weather_label.config(text=f"Weather in {city_name}: {weather}, {temp}", font=("Arial", 16), fg="white", bg="midnight blue")
    else:
        weather_label.config(text=weather_data, font=("Arial", 16), fg="white", bg="midnight blue")

# Create the main window
root = tk.Tk()
root.title("Weather App")
root.configure(bg="midnight blue")

# Create input field for city
city_label = tk.Label(root, text="Enter city:", font=("Arial", 14), fg="white", bg="midnight blue")
city_label.pack(pady=10)
city_entry = tk.Entry(root, font=("Arial", 14))
city_entry.pack(pady=5)

# Create button to fetch weather data
submit_button = tk.Button(root, text="Get Weather", command=display_weather, font=("Arial", 14), bg="light sky blue", activebackground="sky blue")
submit_button.pack(pady=10)

# Create label to display weather information
weather_label = tk.Label(root, text="", font=("Arial", 16), fg="white", bg="midnight blue")
weather_label.pack(pady=20)

# Run the main loop
root.mainloop()
