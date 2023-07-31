import requests, os, dotenv

dotenv.load_dotenv()

API_KEY = os.environ["API_KEY"]

def get_weather_data(city):
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
        response = requests.get(url)
        data = response.json()
        
        if data['cod'] == 200:
            return data
        else:
            return False


