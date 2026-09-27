import requests


WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"


class WeatherAPIError(Exception):
    pass


def get_weather(city, api_key):
    try:
        response = requests.get(
            WEATHER_URL,
            params={
                "q": city,
                "appid": api_key,
                "units": "metric"
            },
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        return {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "condition": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"]
        }

    except requests.exceptions.Timeout:
        raise WeatherAPIError(
            "The weather service took too long to respond."
        )

    except requests.exceptions.ConnectionError:
        raise WeatherAPIError(
            "Could not connect to the weather service."
        )

    except requests.exceptions.HTTPError:
        raise WeatherAPIError(
            f"Weather service returned an error: {response.status_code}"
        )

    except (KeyError, ValueError):
        raise WeatherAPIError(
            "Received an invalid response from the weather service."
        )