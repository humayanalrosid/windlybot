from flask import Flask
from weather import get_weather_data
import os, dotenv, telebot

app = Flask(__name__)
dotenv.load_dotenv()

TOKEN = os.environ["TOKEN"]

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    city = message.text

    if city == "/start":
        bot.send_message(message.chat.id, "Hi! I am Windly, a weather bot. Send me a city name, and I'll send you the weather details.")
    elif city == "/about":
        bot.send_message(message.chat.id, "This bot provides weather details for any city. Simply send a city name, and it'll send you the weather details. You can also use the `/help` command to learn more.")
    elif city == "/developer":
        bot.send_message(message.chat.id, "This bot was created by @humayanar. It was developed using Python.")
    elif city == "/help":
        bot.send_message(message.chat.id, "Simply send a city name, and it'll send you the weather details.\n\n/about - About the bot\n/developer - About the developer\n/help - Help")
    else:
        weather_data = get_weather_data(city)
        
        if not weather_data == False:
            bot.send_message(message.chat.id, format_weather_response(weather_data))
        else:
            bot.send_message(message.chat.id, "Sorry, city not found. Please try again.")


def format_weather_response(data):
    temp =  round(data["main"]["temp"] - 273.15, 2)    
    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]
    wind_speed = data["wind"]["speed"]
    weather = data["weather"][0]["main"]
    city = data["name"]
    country = data["sys"]["country"]
    cloud = data["clouds"]["all"]
    description = data["weather"][0]["description"]
    icon = data["weather"][0]["icon"]
    
    icon = f"https://openweathermap.org/img/w/{icon}.png"
    
    response = f"Current weather in {city}, {country}:\n\nTemperature: {temp}°C\nWeather: {weather}\nHumidity: {humidity}%\nWind: {wind_speed} kph\nPressure: {pressure} mb\nCloud Cover: {cloud}%\nDescription: {description.capitalize()}\n\n{icon}"

    return response

if __name__ == "__main__":
    bot.polling()
    app.run(debug=True)

