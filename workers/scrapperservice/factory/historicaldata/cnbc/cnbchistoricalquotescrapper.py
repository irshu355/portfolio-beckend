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
from datetime import datetime, timedelta
from decimal import Decimal
from django.conf import settings


class CNBCHistoricalQuoteScrapperService:
    def __init__(self, consumer_key, consumer_secret):
        self._key = consumer_key
        self._secret = consumer_secret
        self.name = HistoricalQuoteScrapperSource.CNBC.value

    # #intervals for historical data are determined as below:
    # for accurate intervals, refer to settings.py
    # 1D - 1 Minute
    # 5D - 5M Minutes
    # 1M - 30 Minutes
    # 6M - 1D
    # 1Y - 1W

    def scrap(self, symbol, period):
        now = datetime.now()

        marketOpens = self.todayAt(9, 30, 00)

        day = now.strftime("%A")

        if day == 'Saturday':
            now = marketOpens - timedelta(days=1)
            date_from = now.strftime('%Y%m%d') + "093000"
            date_to = now.strftime('%Y%m%d') + "160000"
        elif day == 'Sunday':
            now = marketOpens - timedelta(days=2)
            date_from = now.strftime('%Y%m%d') + "093000"
            date_to = now.strftime('%Y%m%d') + "160000"
        elif now < marketOpens:
            now = marketOpens - \
                timedelta(
                    days=3) if day == 'Monday' else marketOpens - timedelta(days=1)
            date_from = now.strftime('%Y%m%d') + "093000"
            date_to = now.strftime('%Y%m%d') + "160000"
        else:
            date_from = now.strftime('%Y%m%d') + "093000"
            date_to = now.strftime('%Y%m%d') + "160000"

        # for ref 'https://ts-api.cnbc.com/harmony/app/bars/AAL/30M/20120718000000/20200626000000/adjusted/EST5EDT.json'
        url = 'https://ts-api.cnbc.com/harmony/app/bars/{0}/{1}/{2}/{3}/adjusted/EST5EDT.json'.format(
            symbol, period, date_from, date_to)

        requestResponse = requests.get(url, verify=False)
        if (requestResponse.status_code != 200):
            return [], requestResponse.status_code, requestResponse.reason
        jsonRes = json.loads(requestResponse.text)

        return self.parseTimeSeries(jsonRes, symbol, period), 200, ""

    def parseTimeSeries(self, jsonRes, symbol, period):
        history = jsonRes["barData"]["priceBars"]
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
                "volume": rec["volume"],
                "symbol": symbol,
                "period": period
            }
            series.append(obj)
        return series

    def todayAt(self, hr, min=0, sec=0):
        now = datetime.now()
        return now.replace(hour=hr, minute=min, second=sec)


class CNBCHistoricalQuoteScrapperServiceBuilder:
    def __init__(self):
        self._instance = None

    def __call__(self):
        self._instance = CNBCHistoricalQuoteScrapperService(
            "KeyValue1", "KeyValue2")
        return self._instance

    def authorize(self, key, secret):
        return 'PANDORA_CONSUMER_KEY', 'PANDORA_CONSUMER_SECRET'
