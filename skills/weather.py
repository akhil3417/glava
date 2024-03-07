import requests
from config import OPENWEATHER_APP_ID as weather_api, CITY, COUNTRY


def get_weather(url: str) -> dict:
    """
    Retrieve weather information from the provided URL.

    Args:
        url (str): The URL to retrieve weather information from.

    Returns:
        dict: The weather information in JSON format, or an error message in case of an exception.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred: {e}"}


def weather_report(
    city: str,
    country_code: str = None,
    num_entries: int = 5,
    api_key: str = weather_api,
) -> str:
    """
    Retrieve weather report for a specific city.

    Args:
        city (str): The name of the city.
        country_code (str, optional): The country code of the city. Defaults to None.
        num_entries (int, optional): The number of forecast entries to retrieve. Defaults to 5.
        api_key (str, optional): The API key for accessing weather data. Defaults to weather_api.

    Returns:
        str: The weather report for the specified city.
    """
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}{','+country_code if country_code else '' }&appid={api_key}&units=metric"
    data = get_weather(url)
    if "error" in data:
        return data["error"]
    w = data["weather"][0]["description"]
    t = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    # r = f"Weather in {city}: {w}, Temperature: {t}°C\n\n"
    r = f"The current weather in {city} is {w} with a temperature of {t} degrees Celsius. it feels like {feels_like}\n\n"
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}{','+country_code if country_code else '' }&appid={api_key}&units=metric"
    data = get_weather(url)
    if "error" in data:
        return data["error"]
    r += "5 day / 3 hour forecast:\n"
    # r += f"The forecast for the next {num_entries} days in {city} is:\n"
    for item in data["list"][:num_entries]:
        r += f"Time: {item['dt_txt']}, Weather: {item['weather'][0]['description']}, Temperature: {item['main']['temp']}°C\n"
        # r += f"On {item['dt_txt']}, the weather will be {item['weather'][0]['description']} with a temperature of {item['main']['temp']} degrees Celsius.\n"
    return r.strip()


def weather_report_command():
    """
    This function calls the weather_report function with the CITY, the capitalized COUNTRY, num_entries(int,optional),and api_key(str,optional) as its arguments.
    """
    print(weather_report(CITY, COUNTRY.capitalize(), 5))
