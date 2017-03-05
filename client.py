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

api_key = None

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

        # Processar dades
        data = json.loads(web.text)
        return data["almanac"]

if __name__ == "__main__":
    if not api_key:
        try:
            api_key = sys.argv[1]
        except IndexError:
            print "La API a la linia de comandes"

    wc = WeatherClient(api_key)
    wc.almanac("Lleida")
