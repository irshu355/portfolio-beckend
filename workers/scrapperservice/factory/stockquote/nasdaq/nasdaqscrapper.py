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


class NasdaqScrapperService:

    def __init__(self, consumer_key, consumer_secret):
        self._key = consumer_key
        self._secret = consumer_secret
        self.name = TickerScrapperSource.NASDAQ.value

    def test_connection(self):
        print(f'Accessing Pandora with {self._key} and {self._secret}')

    def scrapTicker(self, ticker):

        # headers = {
        # "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        # "Accept-Encoding":"gzip, deflate",
        # "Accept-Language":"en-GB,en;q=0.9,en-US;q=0.8,ml;q=0.7",
        # "Connection":"keep-alive",
        # "Host":"www.nasdaq.com",
        # "Referer":"http://www.nasdaq.com",
        # "Upgrade-Insecure-Requests":"1",
        # "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36"
        #  }

        #url = 'https://www.nasdaq.com/market-activity/stocks/{}'.format(ticker)

        summaryUrl = "https://api.nasdaq.com/api/quote/{}/summary?assetclass=stocks".format(
            ticker)
        infoUrl = "https://api.nasdaq.com/api/quote/{}/info?assetclass=stocks".format(
            ticker)

        summaryReponse = requests.get(summaryUrl, verify=False)
        infoResponse = requests.get(infoUrl, verify=False)

        if summaryReponse.status_code != 200:
            raise ValueError("Invalid Response Received From Webserver")

        if infoResponse.status_code != 200:
            raise ValueError("Invalid Response Received From Webserver")

        summaryJson = json.loads(summaryReponse.text)
        infoJson = json.loads(infoResponse.text)
        return self.parseJsonTickerResponse(summaryJson, infoJson)

    def parseJsonTickerResponse(self, summaryJson, infoJson):
        symbol = infoJson["data"]["symbol"]
        lastSale = infoJson["data"]["primaryData"]["lastSalePrice"]  # xxxx
        name = infoJson["data"]["companyName"]
        exchange = 0 if infoJson["data"]["exchange"].lower() == "nasdaq" else 1

        # xxxx
        previous_close = infoJson["data"]["keyStats"]["PreviousClose"]["value"]
        volume = infoJson["data"]["keyStats"]["Volume"]["value"]
        pe_ratio = summaryJson["data"]["summaryData"]["PERatio"]["value"]
        # xxxx
        eps = summaryJson["data"]["summaryData"]["EarningsPerShare"]["value"]
        market_cap = infoJson["data"]["keyStats"]["MarketCap"]["value"]
        sector = summaryJson["data"]["summaryData"]["Sector"]["value"]
        industry = summaryJson["data"]["summaryData"]["Industry"]["value"]

        fifty_two_week_low = summaryJson["data"]["summaryData"]["FiftTwoWeekHighLow"]["value"].split(
            "/")[1]  # xxxx
        fifty_two_week_high = summaryJson["data"]["summaryData"]["FiftTwoWeekHighLow"]["value"].split(
            "/")[0]  # xxxx
        day_low = summaryJson["data"]["summaryData"]["TodayHighLow"]["value"].split(
            "/")[1]  # xxxx
        day_high = summaryJson["data"]["summaryData"]["TodayHighLow"]["value"].split(
            "/")[0]  # xxxx

        ninetyDayVolume = summaryJson["data"]["summaryData"]["AverageVolume"]["value"]
        y1Target = summaryJson["data"]["summaryData"]["OneYrTarget"]["value"]
        forwardpe_one_year = summaryJson["data"]["summaryData"]["ForwardPE1Yr"]["value"]
        annualizedDivident = summaryJson["data"]["summaryData"]["AnnualizedDividend"]["value"]
        exDividentDate = summaryJson["data"]["summaryData"]["ExDividendDate"]["value"]

        data = {}
        data["symbol"] = symbol
        data["name"] = name
        data["price"] = float(
            ''.join(e for e in lastSale if e.isdigit() or e == '.'))
        data["sector"] = sector
        data["industry"] = industry
        data["previous_close"] = float(
            ''.join(e for e in previous_close if e.isdigit() or e == '.'))
        data["fifty_two_week_low"] = float(
            ''.join(e for e in fifty_two_week_low if e.isdigit() or e == '.'))
        data["fifty_two_week_high"] = float(
            ''.join(e for e in fifty_two_week_high if e.isdigit() or e == '.'))
        data["day_low"] = float(
            ''.join(e for e in day_low if e.isdigit() or e == '.'))
        data["day_high"] = float(
            ''.join(e for e in day_high if e.isdigit() or e == '.'))
        data["volume"] = int(
            ''.join(e for e in volume if e.isdigit() or e == '.'))
        data["pe_ratio"] = pe_ratio
        data["eps"] = float(''.join(e for e in eps if e.isdigit() or e == '.'))
        data["market_cap"] = int(
            ''.join(e for e in market_cap if e.isdigit() or e == '.'))
        data["exchange"] = exchange

        data["y1target"] = float(
            ''.join(e for e in y1Target if e.isdigit() or e == '.'))
        data["ninety_day_avg_volume"] = int(
            ''.join(e for e in ninetyDayVolume if e.isdigit() or e == '.'))
        data["forwardpe_one_year"] = float(
            ''.join(e for e in forwardpe_one_year if e.isdigit() or e == '.')) if self.hasNumbers(forwardpe_one_year) else 0.00
        data["annual_divident"] = float(
            ''.join(e for e in annualizedDivident if e.isdigit() or e == '.')) if self.hasNumbers(annualizedDivident) else 0.00
        data["ex_divident_date"] = exDividentDate

        return data

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

        tbl_summary_date.find('tbody').find_all(
            "td", text="Previous Close").find_next_sibling("td").text

        symbol = symbol_block.get_text()
        price = price_block.get_text()
        name = name_block.get_text()

        #price, name, previuous_close, year_low,year_high,volume, pe_ratio,eps,market_cap,sector
        print(symbol)

    def hasNumbers(self, inputString):
        return any(char.isdigit() for char in inputString)


class NasdaqScrapperServiceBuilder:
    def __init__(self):
        self._instance = None

    def __call__(self):
        self._instance = NasdaqScrapperService("KeyValue1", "KeyValue2")
        return self._instance

    def authorize(self, key, secret):
        return 'PANDORA_CONSUMER_KEY', 'PANDORA_CONSUMER_SECRET'
