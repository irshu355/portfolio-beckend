import requests
import json
from urllib.request import urlopen, Request
from urllib.parse import urlencode, urlparse, parse_qs
from bs4 import BeautifulSoup
from requests import get
import collections
import string
import os.path
import re
import csv
import json
from workers.models import OptionsScrapperSource


class YFOptionScrapperService:
    def __init__(self, consumer_key, consumer_secret):
        self._key = consumer_key
        self._secret = consumer_secret
        self.name = OptionsScrapperSource.YF.value

    def test_connection(self):
        print(f'Accessing Pandora with {self._key} and {self._secret}')

    def scrapOption(self, ticker):

        url = 'https://query2.finance.yahoo.com/v7/finance/options/{}?formatted=true&lang=en-US&region=US&date=1600387200&corsDomain=finance.yahoo.com'.format(
            ticker)

        requestResponse = requests.get(url, verify=False)
        jsonRes = json.loads(requestResponse.text)
        self.parseResponse(jsonRes)

    def parseResponse(self, json):
        expirations = json["optionChain"]["result"][0]["expirationDates"]
        for expiry in expirations:
            print(expiry)
        pass


class YFOptionScrapperServiceBuilder:
    def __init__(self):
        self._instance = None

    def __call__(self):
        self._instance = YFOptionScrapperService("KeyValue1", "KeyValue2")
        return self._instance

    def authorize(self, key, secret):
        return 'PANDORA_CONSUMER_KEY', 'PANDORA_CONSUMER_SECRET'
