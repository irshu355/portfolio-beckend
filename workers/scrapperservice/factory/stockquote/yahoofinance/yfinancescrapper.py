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
from workers.models import TickerScrapperSource


class YFScrapperService:
    def __init__(self, consumer_key, consumer_secret):
        self._key = consumer_key
        self._secret = consumer_secret
        self.name = TickerScrapperSource.YF.value

    def test_connection(self):
        print(f'Accessing Pandora with {self._key} and {self._secret}')

    def scrapTicker(self, ticker):

        quoteUrl = "https://query2.finance.yahoo.com/v7/finance/options/{}?formatted=true&lang=en-US&region=US&corsDomain=finance.yahoo.com".format(
            ticker)

        quoteResponse = requests.get(quoteUrl, verify=False)
        quoteJson = json.loads(quoteResponse.text)
        return self.parseJsonTickerResponse(quoteJson)

    def parseJsonTickerResponse(self, quoteJson):

        quote = quoteJson["optionChain"]["result"][0]["quote"]

        symbol = quoteJson["optionChain"]["result"][0]["underlyingSymbol"]
        name = quote["longName"]
        price = quote["regularMarketPrice"]
        day_high = quote["regularMarketDayHigh"]
        day_low = quote["regularMarketDayLow"]
        volume = quote["regularMarketVolume"]
        previous_close = quote["regularMarketPreviousClose"]
        exchange = 0 if "nasdaq" in quote["fullExchangeName"].lower() else 1
        # sector,90dayvolume, industry,pe,y1target,
        # divident and ex.DivDate not available
        marketcap = quote["marketCap"]
        fifty_two_week_low = quote["fiftyTwoWeekLow"]
        fifty_two_week_high = quote["fiftyTwoWeekHigh"]
        forwardpe_one_year = quote["forwardPE"]
        eps = quote["epsTrailingTwelveMonths"]

        data = {}

        data["source"] = self.name
        data["symbol"] = symbol
        data["name"] = name
        data["price"] = price
        data["previous_close"] = previous_close
        data["fifty_two_week_low"] = fifty_two_week_low
        data["fifty_two_week_high"] = fifty_two_week_high
        data["day_low"] = day_low
        data["day_high"] = day_high
        data["volume"] = volume
        data["eps"] = eps
        data["market_cap"] = marketcap
        data["exchange"] = exchange

        data["forwardpe_one_year"] = forwardpe_one_year

        return data


class YFinanceScrapperServiceBuilder:
    def __init__(self):
        self._instance = None

    def __call__(self):
        self._instance = YFScrapperService("KeyValue1", "KeyValue2")
        return self._instance

    def authorize(self, key, secret):
        return 'PANDORA_CONSUMER_KEY', 'PANDORA_CONSUMER_SECRET'
