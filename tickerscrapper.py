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


class Scrapper():
    def __init__(self):
        pass


def factory(source):
    class Nasdaq(Scrapper):
        def scrapTicker(self):
            USER_AGENT = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
            google_url = 'https://www.nasdaq.com/market-activity/stocks/{}'.format(
                ticker)
            response = requests.get(google_url, headers=USER_AGENT)
            response.raise_for_status()
            self.parse_results(response.text, ticker)

        def parseTickerResponse(self, response):
            soup = BeautifulSoup(html, 'html.parser')
            found_results = []
            rank = 1
            result_block = soup.find_all(
                'span', attrs={'class': 'symbol-page-header__symbol'})
            symbol = result_block[0].get_text()
            print(symbol)

    class CNBC(source):
        def scrapTicker(self):
            pass

    class MarketWatch(source):
        def scrapTicker(self):
            pass

    def scrapTicker(self, ticker):

    def parse_results(self, html, ticker):
