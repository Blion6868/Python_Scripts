import os
import requests
from dotenv import load_dotenv

def ensure_utf8_env(file_path):
    """Check encoding and convert to UTF-8 if needed."""
    try:
        # Try reading as UTF-8
        with open(file_path, "r", encoding="utf-8") as f:
            f.read()
    except UnicodeDecodeError:
        # If UTF-8 fails, assume UTF-16 and convert
        with open(file_path, "rb") as f:
            raw = f.read()
        text = raw.decode("utf-16")  # Decode as UTF-16
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Converted {file_path} to UTF-8 encoding.")

# Path to your .env file
env_file = "creds.env"
ensure_utf8_env(env_file)

# Load environment variables
load_dotenv(dotenv_path=env_file)

# Get API key
API_KEY = os.getenv("api_key")
if not API_KEY:
    raise ValueError("API key not found. Check creds.env format: api_key=YOUR_KEY")

# Weather API details
CITY = "Sandy,US"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

params = {
    "q": CITY,
    "appid": API_KEY,
    "units": "imperial"
}

try:
    # Disable SSL verification (NOT recommended for production)
    response = requests.get(BASE_URL, params=params, verify=False)
    response.raise_for_status()
    data = response.json()

    city_name = data["name"]
    temp = data["main"]["temp"]
    weather_desc = data["weather"][0]["description"]
    humidity = data["main"]["humidity"]

    print(f"Weather in {city_name}:")
    print(f"Temperature: {temp}°F")
    print(f"Condition: {weather_desc}")
    print(f"Humidity: {humidity}%")

except requests.exceptions.RequestException as e:
    print(f"Error fetching weather data: {e}")

