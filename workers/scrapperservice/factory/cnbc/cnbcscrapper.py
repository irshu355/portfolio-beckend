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


class CNBCScrapperService:

    def __init__(self, consumer_key, consumer_secret):
        self._key = consumer_key
        self._secret = consumer_secret

    def test_connection(self):
        print(f'Accessing Pandora with {self._key} and {self._secret}')

    def scrapTicker(self, ticker):
        USER_AGENT = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
        google_url = 'https://www.nasdaq.com/market-activity/stocks/{}'.format(
            ticker)
        response = requests.get(google_url, headers=USER_AGENT)
        response.raise_for_status()
        self.parseTickerResponse(response.text)

    def parseTickerResponse(self, html):
        soup = BeautifulSoup(html, 'html.parser')

        symbol_block = soup.find_next(
            'span', attrs={'class': 'symbol-page-header__symbol'})
        price_block = soup.find_next(
            'span', attrs={'class': 'symbol-page-header__pricing-price'})

        name_block = soup.find_next(
            'span', attrs={'class': 'symbol-page-header__name'})

        tbl_summary_date = soup.find_next(
            'table', attrs={'class': 'summary-data__table'})
        prev_close_cell = tbl_summary_date.find(
            lambda tag: tag.name == "td" and "Previous Close" in tag.text)
        prev_close_block = prev_close_cell.parent.find_all("td")[-1]

        symbol = symbol_block.get_text()
        price = price_block.get_text()
        name = name_block.get_text()
        prev_close = prev_close_block.text

        #price, name, previuous_close, year_low,year_high,volume, pe_ratio,eps,market_cap,sector
        print(symbol)


class CNBCScrapperServiceBuilder:
    def __init__(self):
        self._instance = None

    def __call__(self):
        self._instance = CNBCScrapperService("KeyValue1", "KeyValue2")
        return self._instance

    def authorize(self, key, secret):
        return 'PANDORA_CONSUMER_KEY', 'PANDORA_CONSUMER_SECRET'
