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
from django.conf import settings


class AlphaVintageHistoricalQuoteScrapperService:
    def __init__(self, consumer_key, consumer_secret):
        self._key = "MSCH79QTH2GCP5RL"
        self._secret = consumer_secret
        self.name = HistoricalQuoteScrapperSource.AlphaVintage.value

    # #intervals for historical data are determined as below:
    # for accurate intervals, refer to settings.py
    # 1D - 1 Minute
    # 5D - 7 Minutes
    # 1M - 30 Minutes
    # 6M - 240 Minutes(4 hrs)
    # 1Y - 480 Minutes(8 hrs)

    def scrap(self, symbol, interval):
        if interval not in(settings.QUOTE_INTRA_DAY_DELAY, 480):
            print("this provider only support 1M or 1D")
            return

        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={0}&interval=1min&apikey={1}&outputsize=full'.format(
            symbol, self._key) if interval == settings.QUOTE_INTRA_DAY_DELAY else 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={0}&outputsize=full&apikey={1}'.format(
            symbol, self._key)

        requestResponse = requests.get(url, verify=False)

        if (requestResponse.status_code != 200):
            return [], requestResponse.status_code, requestResponse.reason
        jsonRes = json.loads(requestResponse.text)

        return self.parseTimeSeries(jsonRes, symbol, interval), 200, ""

    def parseTimeSeries(self, jsonRes, symbol, interval):
        seriesObj = jsonRes["Time Series (1min)"] if interval == settings.QUOTE_INTRA_DAY_DELAY else jsonRes["Time Series (Daily)"]
        series = []
        for time in seriesObj.keys():

            datetime_object = datetime.strptime(
                time if interval == settings.QUOTE_INTRA_DAY_DELAY else time+" 16:00:00", '%Y-%m-%d %H:%M:%S')
            obj = {
                "open": float(seriesObj[time]["1. open"]),
                "high": float(seriesObj[time]["2. high"]),
                "low": float(seriesObj[time]["3. low"]),
                "close": float(seriesObj[time]["4. close"]),
                "volume": float(seriesObj[time]["5. volume"]),
                "symbol": symbol,
                "timestamp": datetime_object
            }
            series.append(obj)
        return series


class AlphaVintageHistoricalQuoteScrapperServiceBuilder:
    def __init__(self):
        self._instance = None

    def __call__(self):
        self._instance = AlphaVintageHistoricalQuoteScrapperService(
            "KeyValue1", "KeyValue2")
        return self._instance

    def authorize(self, key, secret):
        return 'PANDORA_CONSUMER_KEY', 'PANDORA_CONSUMER_SECRET'
