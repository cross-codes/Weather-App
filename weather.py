# weather.py

from configparser import ConfigParser
import argparse
import sys
import style
import requests

BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Weather condition codes:
THUNDERSTORM = range(200, 300)
DRIZZLE = range(300, 400)
RAIN = range(500, 600)
SNOW = range(600, 700)
ATMOSPHERE = range(700, 800)
CLEAR = range(800, 801)
CLOUDY = range(801, 900)


def _get_key():  # _<>() implies the function is non-public
    configuration = ConfigParser()
    configuration.read("secrets.ini")
    return configuration["OpenWeather"]["api_key"]


def read_user_cli_arguments():
    parser = argparse.ArgumentParser(
        description="Gets weather and temperature information"
    )
    parser.add_argument("city", nargs="+", type=str, help="Enter the city name")
    parser.add_argument(
        "-i",
        "--imperial",
        action="store_true",
        help="Display the temperature in imperial units",
    )
    return parser.parse_args()


def get_weather_data(city_input, imperial=False):
    api_key = _get_key()
    city_name = " ".join(city_input).strip()

    if imperial:
        units = "imperial"
    else:
        units = "metric"

    response = requests.get(
        BASE_URL, params={"q": city_name, "units": units, "appid": api_key}
    )

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        sys.exit("Error: API key invalid.")
    elif response.status_code == 404:
        sys.exit("Error: Cannot find weather data for this city, if it exists.")
    else:
        errormessage = (
            "Something went wrong... (Error code: {err}, Response: {response}).".format(
                err=response.status_code, response=response.content
            )
        )
        sys.exit(errormessage)


def display_weather_info(weather_data, imperial=False):
    weather_id = weather_data["weather"][0]["id"]
    if weather_id in THUNDERSTORM:
        x = style.change_colour(style.RED)
    elif weather_id in DRIZZLE:
        x = style.change_colour(style.CYAN)
    elif weather_id in RAIN:
        x = style.change_colour(style.BLUE)
    elif weather_id in SNOW:
        x = style.change_colour(style.WHITE)
    elif weather_id in ATMOSPHERE:
        x = style.change_colour(style.BLUE)
    elif weather_id in CLEAR:
        x = style.change_colour(style.YELLOW)
    elif weather_id in CLOUDY:
        x = style.change_colour(style.WHITE)
    else:
        x = style.change_colour(style.RESET)

    if imperial:
        out = """\n{REVERSE}Name: {name}{RESET}\nCoordinates (Latitude/Longitude): {latitude}/{longitude}
        \b\b\b\b\b\b\b\b\b{COLOUR}Weather Data {RESET_COLOUR}:
        \tDescription: {DESC_COLOUR}{description}{RESET_DESC_COLOUR}
        \tTemperature: {temp}°F
        \tTemperature feels like: {feel}°F
        \tHumidity: {humidity}%
        \tPressure: {pressure} hPa\n""".format(
            REVERSE=style.change_colour(style.REVERSE),
            name=weather_data["name"],
            RESET=style.change_colour(style.RESET),
            latitude=weather_data["coord"]["lat"],
            longitude=weather_data["coord"]["lon"],
            COLOUR=style.change_colour(style.CYAN),
            RESET_COLOUR=style.change_colour(style.RESET),
            DESC_COLOUR=x,
            RESET_DESC_COLOUR=style.change_colour(style.RESET),
            description=weather_data["weather"][0]["description"].capitalize(),
            temp=weather_data["main"]["temp"],
            feel=weather_data["main"]["feels_like"],
            humidity=weather_data["main"]["humidity"],
            pressure=weather_data["main"]["pressure"],
        )
    else:
        out = """\n{REVERSE}Name: {name}{RESET}\nCoordinates (Latitude/Longitude): {latitude}/{longitude}
        \b\b\b\b\b\b\b\b\b{COLOUR}Weather Data {RESET_COLOUR}:
        \tDescription: {DESC_COLOUR}{description}{RESET_DESC_COLOUR}
        \tTemperature: {temp}°C
        \tTemperature feels like: {feel}°C
        \tHumidity: {humidity}%
        \tPressure: {pressure} hPa\n""".format(
            REVERSE=style.change_colour(style.REVERSE),
            name=weather_data["name"],
            RESET=style.change_colour(style.RESET),
            latitude=weather_data["coord"]["lat"],
            longitude=weather_data["coord"]["lon"],
            COLOUR=style.change_colour(style.CYAN),
            RESET_COLOUR=style.change_colour(style.RESET),
            DESC_COLOUR=x,
            RESET_DESC_COLOUR=style.change_colour(style.RESET),
            description=weather_data["weather"][0]["description"].capitalize(),
            temp=weather_data["main"]["temp"],
            feel=weather_data["main"]["feels_like"],
            humidity=weather_data["main"]["humidity"],
            pressure=weather_data["main"]["pressure"],
        )
    return out


if __name__ == "__main__":
    user_arguments = read_user_cli_arguments()
    weather_data = get_weather_data(user_arguments.city, user_arguments.imperial)
    print(display_weather_info(weather_data, user_arguments.imperial))
