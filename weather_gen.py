#!/usr/bin/env python

#-*- coding: utf-8 -*-

import json
from jinja2 import Template
import sys
import argparse

weather_type = {
        "suny": u'Солнечно',
        "rainy": u'Дождливо',
        "cloudy": u'Облачно',
        "subcloudy": u'Переменная облачность',
        "bitrainy": u'Слабый дождь',
        "windy": u'Ветренно',
        "storm": u'Гроза',
        }

weather_icon = {
        "suny": "Suny.svg",
        "rainy": "rainy.svg",
        "cloudy": "Cloudy.svg",
        "subcloudy": "subcoudy.svg",
        "bitrainy": "bitrainy.svg",
        "windy": "windy.svg",
        "storm": "storm.svg",
        }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", action = "store", default = "/var/www/html/",\
                         help = "Sets path to write output html")
    parser.add_argument("-j", "--json", action = "store", help = "Sets weather in json format")
    args = parser.parse_args()
    
    weather = json.loads(args.json)
    config={}
    config['temp'] = weather['temp']
    config['speed'] = weather['wind']['speed'] + u'м/с'
    config['weather'] = weather_type[weather['weather']]
    config['ico'] = "img/weather/" + weather_icon[weather['weather']]


    result = RenderTemplate("weather.j2", config)
    fpage = codecs.open(args.output + "weather.html", "w", "utf-8")        
    fpage.write(result)
    fpage.close()


if __name__ == "__main__":
    sys.exit(main())
