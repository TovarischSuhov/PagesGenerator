from jinja2 import Template
import requests
import sys
import argparse

weather_pics = { "rain": "img/weather/",
                 "storm": "img/weather/",
                 "cloudy": "img/weather/",
                 "suny": "img/weather/",
                 "temp_cloudy": "img/weather/"}
wind_pics = { "N": "img/weather/north.png",
              "NE": "img/weather/north-east.png",
              "E": "img/weather/east.png",
              "SE": "img/weather/south-east.png",
              "S": "img/weather/south.png",
              "SW": "img/weather/south-west.png",
              "W": "img/weather/west.png",
              "NW": "img/weather/north-west.png"}


def get_weather():


def main():
    #get params
    weather = get_weather()
    weather_args[temp] = weather.temp
    weather_args[wind_speed] = weather.wind.speed
    weather_contents = RenderTemplate("weather.j2", weather_args)
    #write page


if __name__ == "__main__":
    sys.exit(main())
