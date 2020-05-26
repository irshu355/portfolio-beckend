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
from workers.models import HistoricalQuoteScrapperSource
from datetime import datetime
from decimal import Decimal


class CNBCHistoricalQuoteScrapperService:
    def __init__(self, consumer_key, consumer_secret):
        self._key = consumer_key
        self._secret = consumer_secret
        self.name = HistoricalQuoteScrapperSource.AlphaVintage.value

    #
    # #intervals for historical data are determined as below:
    # 1D - 1 Minute
    # 5D - 7 Minutes
    # 1M - 30 Minutes
    # 6M - 240 Minutes(4 hrs)
    # 1Y - 480 Minutes(8 hrs)

    def scrap(self, symbol, interval):
        # https://ts-api.cnbc.com/harmony/app/bars/AAL/30M/20120718000000/20200626000000/adjusted/EST5EDT.json
        pass

    def parseTimeSeries(self, jsonRes, symbol, interval):
        history = jsonRes["history"]["priceBars"]
        series = []

        for rec in history:
            datetime_object = datetime.strptime(
                rec["tradeTime"], '%Y%m%d%H%M%S')
            obj = {
                "open": float(rec["open"]),
                "close": float(rec["close"]),
                "high": float(rec["high"]),
                "low": float(rec["low"]),
                "timestamp": datetime_object,
                "volume": float(rec["volume"]),
                "symbol": symbol
            }
            series.append(obj)
        return series


class CNBCHistoricalQuoteScrapperServiceBuilder:
    def __init__(self):
        self._instance = None

    def __call__(self):
        self._instance = CNBCHistoricalQuoteScrapperService(
            "KeyValue1", "KeyValue2")
        return self._instance

    def authorize(self, key, secret):
        return 'PANDORA_CONSUMER_KEY', 'PANDORA_CONSUMER_SECRET'
