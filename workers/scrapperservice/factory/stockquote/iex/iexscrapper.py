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
from django.conf import settings


class IEXScrapperService:

    def __init__(self, consumer_key, consumer_secret):
        self._key = consumer_key
        self._secret = consumer_secret
        self.name = TickerScrapperSource.IEX.value

    def test_connection(self):
        print(f'Accessing IEX with {self._key} and {self._secret}')

    def scrapTicker(self, ticker):

        companyUrl = "https://cloud.iexapis.com/stable/stock/{0}/company?token={1}".format(
            ticker, settings.IEX_TOKEN)

        quoteUrl = "https://cloud.iexapis.com/stable/stock/{0}/quote?token={1}".format(
            ticker, settings.IEX_TOKEN)

        companyResponse = requests.get(
            companyUrl, verify=False)

        quoteResponse = requests.get(
            quoteUrl, verify=False)

        if companyResponse.status_code != 200:
            raise ValueError("Invalid Response Received From Webserver")

        if quoteResponse.status_code != 200:
            raise ValueError("Invalid Response Received From Webserver")

        companyJson = json.loads(companyResponse.text)
        quoteJson = json.loads(quoteResponse.text)
        return self.parseJsonTickerResponse(companyJson, quoteJson)

    def parseJsonTickerResponse(self, companyJson, quoteJson):
        symbol = companyJson["symbol"]
        name = companyJson["companyName"]
        exchange = companyJson["exchange"]
        sector = companyJson["sector"]
        industry = companyJson["industry"]

        price = quoteJson["latestPrice"]
        previous_close = quoteJson["previousClose"]
        fifty_two_week_low = quoteJson["week52Low"]
        fifty_two_week_high = quoteJson["week52High"]
        day_low = quoteJson["low"]
        day_high = quoteJson["high"]
        volume = quoteJson["volume"]
        pe_ratio = quoteJson["peRatio"]
        market_cap = quoteJson["marketCap"]
        eps = 0.0  # only available from financials endpoint, use it
        ninety_day_avg_volume = quoteJson["avgTotalVolume"]

        data = {}
        data["source"] = self.name
        data["symbol"] = symbol
        data["name"] = name
        data["exchange"] = 0 if exchange.lower() == "nasdaq" else 1
        data["sector"] = sector
        data["industry"] = industry
        data["price"] = price
        data["previous_close"] = previous_close
        data["fifty_two_week_low"] = fifty_two_week_low
        data["fifty_two_week_high"] = fifty_two_week_high
        data["day_low"] = day_low
        data["day_high"] = day_high
        data["volume"] = volume
        data["pe_ratio"] = pe_ratio
        data["market_cap"] = market_cap
        data["eps"] = eps
        data["ninety_day_avg_volume"] = ninety_day_avg_volume

        return data

    # eps = models.DecimalField(
    #     max_digits=20, decimal_places=10, blank=True, null=True)

    # y1target = models.DecimalField(
    #     max_digits=20, decimal_places=10, blank=True, null=True)

    # forwardpe_one_year = models.DecimalField(
    #     max_digits=20, decimal_places=10, blank=True, null=True)

    # annual_divident = models.DecimalField(
    #     max_digits=20, decimal_places=10, blank=True, null=True)

    # ex_divident_date = models.CharField(
    #     unique=False, max_length=100, blank=True, null=True)

    # exchange = models.IntegerField(blank=True, null=True)


class IEXScrapperServiceBuilder:
    def __init__(self):
        self._instance = None

    def __call__(self):
        self._instance = IEXScrapperService("KeyValue1", "KeyValue2")
        return self._instance

    def authorize(self, key, secret):
        return 'PANDORA_CONSUMER_KEY', 'PANDORA_CONSUMER_SECRET'
