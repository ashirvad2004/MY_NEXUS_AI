
import requests
import re


def get_weather(city):

    try:
        # Step 1: Get city coordinates
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"

        geo_params = {
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json"
        }

        geo_response = requests.get(
            geo_url,
            params=geo_params,
            timeout=10
        )

        geo_response.raise_for_status()
        geo_data = geo_response.json()

        if not geo_data.get("results"):
            return "City not found. Please check the city name."

        location = geo_data["results"][0]

        latitude = location["latitude"]
        longitude = location["longitude"]
        city_name = location["name"]
        country = location.get("country", "")

        # Step 2: Get weather information
        weather_url = "https://api.open-meteo.com/v1/forecast"

        weather_params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": [
                "temperature_2m",
                "relative_humidity_2m",
                "apparent_temperature",
                "precipitation",
                "weather_code",
                "wind_speed_10m"
            ],
            "timezone": "auto"
        }

        weather_response = requests.get(
            weather_url,
            params=weather_params,
            timeout=10
        )

        weather_response.raise_for_status()
        weather_data = weather_response.json()

        current = weather_data["current"]

        # Step 3: Weather code descriptions
        weather_conditions = {
            0: "Clear Sky",
            1: "Mainly Clear",
            2: "Partly Cloudy",
            3: "Overcast",
            45: "Foggy",
            48: "Depositing Rime Fog",
            51: "Light Drizzle",
            53: "Moderate Drizzle",
            55: "Dense Drizzle",
            61: "Slight Rain",
            63: "Moderate Rain",
            65: "Heavy Rain",
            71: "Slight Snow",
            73: "Moderate Snow",
            75: "Heavy Snow",
            80: "Rain Showers",
            81: "Moderate Rain Showers",
            82: "Violent Rain Showers",
            95: "Thunderstorm"
        }

        condition = weather_conditions.get(
            current["weather_code"],
            "Unknown Weather Condition"
        )

        # Step 4: Prepare readable response
        result = f"""
Weather Report for {city_name}, {country}

Temperature: {current['temperature_2m']}°C
Feels Like: {current['apparent_temperature']}°C
Humidity: {current['relative_humidity_2m']}%
Precipitation: {current['precipitation']} mm
Wind Speed: {current['wind_speed_10m']} km/h

Weather Condition: {condition}
"""

        return result

    except requests.exceptions.RequestException as e:
        return f"Weather API error: {str(e)}"

    except Exception as e:
        return f"Error: {str(e)}"

def get_weather_forecast(city):

    try:
        # Step 1: Get city coordinates
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"

        geo_params = {
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json"
        }

        geo_response = requests.get(
            geo_url,
            params=geo_params,
            timeout=10
        )

        geo_response.raise_for_status()
        geo_data = geo_response.json()

        if not geo_data.get("results"):
            return "City not found."

        location = geo_data["results"][0]

        latitude = location["latitude"]
        longitude = location["longitude"]
        city_name = location["name"]
        country = location.get("country", "")

        # Step 2: Get 7-day forecast
        weather_url = "https://api.open-meteo.com/v1/forecast"

        weather_params = {
            "latitude": latitude,
            "longitude": longitude,
            "daily": [
                "temperature_2m_max",
                "temperature_2m_min",
                "precipitation_probability_max",
                "weather_code"
            ],
            "forecast_days": 7,
            "timezone": "auto"
        }

        response = requests.get(
            weather_url,
            params=weather_params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()
        daily = data["daily"]

        # Step 3: Weather descriptions
        weather_conditions = {
            0: "Clear Sky",
            1: "Mainly Clear",
            2: "Partly Cloudy",
            3: "Overcast",
            45: "Foggy",
            48: "Foggy",
            51: "Light Drizzle",
            53: "Moderate Drizzle",
            55: "Heavy Drizzle",
            61: "Light Rain",
            63: "Moderate Rain",
            65: "Heavy Rain",
            71: "Light Snow",
            73: "Moderate Snow",
            75: "Heavy Snow",
            80: "Rain Showers",
            81: "Moderate Rain Showers",
            82: "Heavy Rain Showers",
            95: "Thunderstorm"
        }

        # Step 4: Prepare forecast
        result = f"7-Day Weather Forecast for {city_name}, {country}\n"

        for i in range(len(daily["time"])):

            date = daily["time"][i]

            max_temp = daily["temperature_2m_max"][i]
            min_temp = daily["temperature_2m_min"][i]

            rain = daily["precipitation_probability_max"][i]

            code = daily["weather_code"][i]

            condition = weather_conditions.get(
                code,
                "Unknown"
            )

            result += f"""
            
Date: {date}
Maximum Temperature: {max_temp}°C
Minimum Temperature: {min_temp}°C
Rain Probability: {rain}%
Condition: {condition}

"""

        return result

    except requests.exceptions.RequestException as e:
        return f"Weather API error: {str(e)}"

    except Exception as e:
        return f"Error: {str(e)}"


# Step 5: Extract city from user query
def extract_city(message):

    patterns = [
        r"\b(?:in|at|for)\s+([a-zA-Z\s.-]+?)(?:\s+(?:today|tomorrow|now|currently|right now)|[?.!,]|$)"
    ]

    for pattern in patterns:

        match = re.search(pattern, message, re.IGNORECASE)

        if match:
            return match.group(1).strip()

    return None
