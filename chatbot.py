from google import genai


MODEL = "gemini-3.5-flash-lite"


def extract_city(question, api_key):
    client = genai.Client(api_key=api_key)

    prompt = f"""
Extract the city name from this weather question.

Rules:
- Return ONLY the city name.
- Do not return a sentence.
- Do not use quotes.
- If there is no city, return NONE.
- Do not invent a city.

Question:
{question}
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
    )

    city = response.text.strip()

    if city.upper() == "NONE":
        return ""

    return city


def generate_weather_response(weather, question, intent, api_key):
    client = genai.Client(api_key=api_key)

    prompt = f"""
You are a weather assistant.

Weather data:
City: {weather["city"]}
Country: {weather["country"]}
Temperature: {weather["temperature"]}°C
Feels like: {weather["feels_like"]}°C
Condition: {weather["condition"]}
Humidity: {weather["humidity"]}%
Wind speed: {weather["wind_speed"]} m/s

User question:
{question}

Detected intent:
{intent}

Rules:

If the intent is weather_query:
- Give a short general summary of the current weather.

If the intent is temperature_query:
- Focus mainly on temperature and feels-like temperature.

If the intent is humidity_query:
- Focus mainly on humidity.

If the intent is wind_query:
- Focus mainly on wind speed and wind conditions.

Use ONLY the provided weather data.
Do not invent information.
Do not provide forecasts.
Answer naturally in 1-3 sentences.
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
    )

    return response.text.strip()