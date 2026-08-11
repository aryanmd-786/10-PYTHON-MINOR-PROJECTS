
import requests
from datetime import datetime

# ------------------- HELPER FUNCTIONS -------------------

def get_coordinates(city_name):
    """
    Open-Meteo Geocoding API se city ke coordinates fetch karna.
    Returns: (latitude, longitude, full_name, country) ya (None, None, None, None)
    """
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Agar error (404, 500) aaya toh exception throw karega
        data = response.json()
        
        if data.get("results"):
            result = data["results"][0]
            lat = result["latitude"]
            lon = result["longitude"]
            name = result["name"]
            country = result.get("country", "Unknown")
            return lat, lon, name, country
        else:
            return None, None, None, None
    except requests.exceptions.RequestException as e:
        print(f"❌ Network/API Error (Geocoding): {e}")
        return None, None, None, None

def get_weather_forecast(lat, lon):
    """
    Open-Meteo Weather API se current weather + 3-day forecast fetch karna.
    Returns: Dictionary with 'current' and 'daily' data, ya None on error.
    """
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&current_weather=true"
        f"&daily=temperature_2m_max,temperature_2m_min,weathercode"
        f"&timezone=auto"
        f"&forecast_days=3"   # Aaj, Kal, Aur Parso
    )
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Network/API Error (Weather): {e}")
        return None

def interpret_weather_code(code):
    """
    WMO weather codes ko human-readable text mein convert karna.
    Official list: https://open-meteo.com/en/docs
    """
    weather_map = {
        0: "☀️ Clear sky", 1: "🌤️ Mainly clear", 2: "⛅ Partly cloudy", 3: "☁️ Overcast",
        45: "🌫️ Fog", 48: "🌫️ Depositing rime fog",
        51: "🌧️ Light drizzle", 53: "🌧️ Moderate drizzle", 55: "🌧️ Dense drizzle",
        61: "🌧️ Slight rain", 63: "🌧️ Moderate rain", 65: "🌧️ Heavy rain",
        71: "❄️ Slight snow", 73: "❄️ Moderate snow", 75: "❄️ Heavy snow",
        80: "🌦️ Slight rain showers", 81: "🌦️ Moderate rain showers", 82: "🌦️ Violent rain showers",
        95: "⛈️ Thunderstorm", 96: "⛈️ Thunderstorm with slight hail", 99: "⛈️ Thunderstorm with heavy hail"
    }
    return weather_map.get(code, f"❓ Unknown ({code})")

def display_forecast(daily_data):
    """
    Daily forecast ko beautifully print karna.
    """
    if not daily_data:
        print("No forecast data available.")
        return
    
    dates = daily_data.get("time", [])
    max_temps = daily_data.get("temperature_2m_max", [])
    min_temps = daily_data.get("temperature_2m_min", [])
    codes = daily_data.get("weathercode", [])
    
    print("\n📅 3-Day Forecast:")
    print("-" * 50)
    for i in range(len(dates)):
        # Date ko readable format mein badalna (e.g., "2026-08-11" -> "11 Aug")
        date_obj = datetime.strptime(dates[i], "%Y-%m-%d")
        date_str = date_obj.strftime("%d %b")
        
        condition = interpret_weather_code(codes[i])
        print(f"{date_str}  |  Max: {max_temps[i]}°C  |  Min: {min_temps[i]}°C  |  {condition}")
    print("-" * 50)

# ------------------- MAIN PROGRAM -------------------

def main():
    print("🌍 === Weather Forecast Mini Project (API based) === 🌍")
    city = input("Enter city name (e.g., London, Mumbai, New York): ").strip()
    
    if not city:
        print("⚠️ City name cannot be empty!")
        return

    # Step 1: City ke coordinates lo
    print(f"🔍 Searching for '{city}'...")
    lat, lon, full_name, country = get_coordinates(city)
    
    if lat is None:
        print(f"❌ City '{city}' not found. Please check spelling.")
        return
    
    print(f"✅ Found: {full_name}, {country} (Lat: {lat}, Lon: {lon})")
    
    # Step 2: Weather data lo
    print("⏳ Fetching weather data...")
    data = get_weather_forecast(lat, lon)
    
    if data is None:
        print("❌ Failed to fetch weather. Please try again later.")
        return

    # Step 3: Current weather print karo
    current = data.get("current_weather", {})
    if current:
        temp = current.get("temperature")
        wind = current.get("windspeed")
        code = current.get("weathercode")
        condition = interpret_weather_code(code)
        
        print("\n" + "=" * 50)
        print(f"📍 {full_name}, {country}")
        print(f"🌡️  Current Temperature: {temp}°C")
        print(f"💨 Wind Speed: {wind} km/h")
        print(f"☁️  Condition: {condition}")
        print("=" * 50)
    else:
        print("⚠️ Current weather data not available.")

    # Step 4: 3-day forecast print karo
    daily = data.get("daily")
    if daily:
        display_forecast(daily)
    else:
        print("⚠️ Daily forecast data not available.")

    print("\n✅ Thank you for using the Weather App!")

# ------------------- RUN -------------------
if __name__ == "__main__":
    main()