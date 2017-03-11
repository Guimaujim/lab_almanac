#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding-utf8 -
'''
Simple client web per temps

@author: guimaujim@gmail.com
'''

import sys
import requests
import json
import time

api_key = None
hour = int(time.strftime("%H"))+1

class WeatherClient(object):
    """Client for Weather underground"""
    url_base = 'http://api.wunderground.com/weather/api/'
    url_service = {"almanac": "/almanac/q/CA/",
                   "hourly": "/hourly/q/CA/"}

    def __init__(self, api_key):
        self.api_key = api_key

    def almanac(self, location):
        # Obtenir https://www.wunderground.com/weather/api/17afbc550df2656e/
        # Obtenir URL
        url = WeatherClient.url_base + self.api_key + \
              WeatherClient.url_service["almanac"] + location + "." + "json"
        web = requests.get(url)

        # Retornar dades
        data = json.loads(web.text)
        return data["almanac"]

    def hourly(self, location):
        # Obtenir https://www.wunderground.com/weather/api/17afbc550df2656e/
        # Obtenir URL
        url = WeatherClient.url_base + self.api_key + \
              WeatherClient.url_service["hourly"] + location + "." + "json"
        web = requests.get(url)

        data = json.loads(web.text)
        return data["hourly_forecast"]


def print_almanac(almanac_data):
    # Imprimir temperatures record, i mitjana actual altes
    print "Max. temperatures:"
    print "Record max. of %s C in the year %s today" % (almanac_data["temp_high"]["record"]["C"], almanac_data["temp_high"]["recordyear"])
    print "Average of %s C in today's date" % (almanac_data["temp_high"]["normal"]["C"])
    # Imprimir temperatures record, i mitjana actual baixes
    print "Min. temperatures:"
    print "Record min. of %s C in the year %s today" % (almanac_data["temp_low"]["record"]["C"], almanac_data["temp_low"]["recordyear"])
    print "Average of %s C in today's date" % (almanac_data["temp_low"]["normal"]["C"])
    print "------------------------------------------------"

def print_hourly(hourly_data):
    # Imprimir temps, temperatura, sensacio termica, humitat i vent actuals
    current = hourly_data[0]
    rain = False
    hot = False
    print "Current weather:"
    print "Condition: %s" % (current["condition"])
    print "Temperature: %s C" % (current["temp"]["metric"])
    print "Thermal sensation: %s C" % (current["feelslike"]["metric"])
    print "Wind speed: %s Km/h" % (current["wspd"]["metric"])
    print "Humidity: %s %%" % (current["humidity"])
    print "------------------------------------------------"
    # Imprimir temps futur, agafant de 4 hores en 4 hores ens dona un bon rang de temperatures
    for i in range (4, 24 - hour, 4):
        current = hourly_data[i]
        current_hour = hour + i
        print "Weather at %s h:" % (current_hour)
        print "Condition: %s" % (current["condition"])
        print "Temperature: %s C" % (current["temp"]["metric"])
        print "Thermal sensation: %s C" % (current["feelslike"]["metric"])
        print "Wind speed: %s Km/h" % (current["wspd"]["metric"])
        print "Humidity: %s %%" % (current["humidity"])
        print "------------------------------------------------"

        if 10 <= int(current["fctcode"]) >= 15:
            rain = True
        if int(current["temp"]["metric"]) >= 30:
            hot = True
    # Fer prediccio
    if hot == True:
        print "It's going to be really hot today, it's a good day to go to the swimming pool or the beach!"
    if(int(current["temp"]["metric"]) < 20):
        print "It's going to get cold at night, bring a jacket if you go outside!"
    if rain == True:
        print "It's going to rain, be sure to bring an umbrella!"


if __name__ == "__main__":
    if not api_key:
        try:
            api_key = sys.argv[1]
        except IndexError:
            print "La API a la linia de comandes"

    wc = WeatherClient(api_key)
    print_almanac(wc.almanac("Lleida"))
    print_hourly(wc.hourly("Lleida"))
