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

class WeatherClient(object):
    """Client for Weather underground"""
    url_base = 'http://api.wunderground.com/weather/api/'
    url_service = {"almanac": "/almanac/q/CA/",
                   "hourly": "/hourly/q/CA/"}
    today = time.strftime("%d")

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
    print "Temperatures altes:"
    print "Record maxim de %s C l'any %s en el dia d'avui" % (almanac_data["temp_high"]["record"]["C"], almanac_data["temp_high"]["recordyear"])
    print "Mitjana de maxim de temperatura durant el dia: %s C" % (almanac_data["temp_high"]["normal"]["C"])
    # Imprimir temperatures record, i mitjana actual baixes
    print "Record minim de %s C l'any %s en el dia d'avui" % (almanac_data["temp_low"]["record"]["C"], almanac_data["temp_low"]["recordyear"])
    print "Mitjana de maxim de temperatura durant el dia: %s C" % (almanac_data["temp_low"]["normal"]["C"])

if __name__ == "__main__":
    if not api_key:
        try:
            api_key = sys.argv[1]
        except IndexError:
            print "La API a la linia de comandes"

    wc = WeatherClient(api_key)
    print_almanac(wc.almanac("Lleida"))
    wc.hourly("Lleida")
