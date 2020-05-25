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
from datetime import datetime
from decimal import Decimal


class YFOptionScrapperService:
    def __init__(self, consumer_key, consumer_secret):
        self._key = consumer_key
        self._secret = consumer_secret
        self.name = OptionsScrapperSource.YF.value

    def test_connection(self):
        print(f'Accessing Pandora with {self._key} and {self._secret}')

    def scrapOption(self, ticker):

        url = 'https://query2.finance.yahoo.com/v7/finance/options/{}?formatted=true&lang=en-US&region=US&corsDomain=finance.yahoo.com'.format(
            ticker)

        requestResponse = requests.get(url, verify=False)
        jsonRes = json.loads(requestResponse.text)
        expirations = self.parseExpirations(jsonRes)
        contracts, status, reason = self.scraptContracts(ticker, expirations)
        return contracts, status, reason

    def scraptContracts(self, ticker, expirations):
        contracts = []
        for exp in expirations:
            url = 'https://query2.finance.yahoo.com/v7/finance/options/{0}?formatted=true&lang=en-US&region=US&date={1}&corsDomain=finance.yahoo.com'.format(
                ticker, exp)
            requestResponse = requests.get(url, verify=False)

            if (requestResponse.status_code != 200):
                return [], requestResponse.status_code, requestResponse.reason

            jsonRes = json.loads(requestResponse.text)

            if 'finance' in jsonRes:
                if jsonRes["finance"]["error"]["code"]:
                    continue

            if 'optionChain' in jsonRes:
                options = jsonRes["optionChain"]["result"][0]["options"]
            else:
                options = jsonRes["options"]

            calls = options[0]["calls"]
            puts = options[0]["puts"]

            for c in calls:
                obj = self.getOptionObj(c, exp, ticker)
                obj["contract_type"] = "C"
                obj["contract_name"] = self.buildContractName(
                    "C", c, exp, ticker)
                contracts.append(obj)

            for p in puts:
                obj = self.getOptionObj(p, exp, ticker)
                obj["contract_type"] = "P"
                obj["contract_name"] = self.buildContractName(
                    "P", p, exp, ticker)
                contracts.append(obj)
        return contracts, 200, ""

    def buildContractName(self, type, contractObj, timestamp, symbol):
        expires = datetime.fromtimestamp(timestamp)
        exp = expires.strftime("%m%d%y")
        strike = '{:.2f}'.format(contractObj["strike"]["raw"])
        contractName = type + symbol + "-" + exp + strike
        return contractName

    def getOptionObj(self, contractObj, timestamp, underlyingSymbol):
        obj = {}
        obj["symbol"] = underlyingSymbol
        obj["strike"] = contractObj["strike"]["raw"]

        if 'impliedVolatility' in contractObj:

            obj["iv"] = self.getSanitizedDecimal(
                contractObj["impliedVolatility"]["raw"])
            #obj["iv"] = 1.00

        if 'change' in contractObj:
            obj["change"] = self.getSanitizedDecimal(
                contractObj["change"]["raw"])

        if 'volume' in contractObj:
            obj["volume"] = contractObj["volume"]["raw"]

        if 'openInterest' in contractObj:
            obj["open_interest"] = contractObj["openInterest"]["raw"]

        if 'ask' in contractObj:
            obj["ask"] = self.getSanitizedDecimal(contractObj["ask"]["raw"])

        if 'bid' in contractObj:
            obj["bid"] = self.getSanitizedDecimal(contractObj["bid"]["raw"])

        if 'last_price' in contractObj:
            obj["last_price"] = self.getSanitizedDecimal(
                contractObj["lastPrice"]["raw"])

        expires = datetime.fromtimestamp(timestamp).date()

        if 'lastTradeDate' in contractObj:
            obj["last_trade_date"] = datetime.fromtimestamp(
                contractObj["lastTradeDate"]["raw"])

        obj["expires"] = expires

        return obj

    #             contract_name = models.CharField(
    #     unique=True, max_length=100, blank=False, null=False)

    # ticker = models.ForeignKey(Ticker,
    #                            on_delete=models.CASCADE)

    # contract_type = models.CharField(
    #     unique=False, max_length=1, blank=False, null=False)
    # strike = models.DecimalField(
    #     max_digits=8, decimal_places=2)
    # iv = models.DecimalField(
    #     max_digits=10, decimal_places=2)
    # change = models.DecimalField(
    #     max_digits=10, decimal_places=2, blank=True, null=True)
    # volume = models.IntegerField(blank=True, null=True)
    # ask = models.DecimalField(
    #     max_digits=8, decimal_places=2)
    # bid = models.DecimalField(
    #     max_digits=8, decimal_places=2)
    # last_price = models.DecimalField(
    #     max_digits=8, decimal_places=2, blank=False, null=False)
    # expires = models.DateTimeField(null=False, blank=False)
    # created = models.DateTimeField(default=now, editable=False)
    # updated = models.DateTimeField(auto_now=True)

    def parseExpirations(self, json):
        expirations = json["optionChain"]["result"][0]["expirationDates"]
        return expirations

    def getSanitizedDecimal(self, value):
        toDecimal = Decimal(value)
        return round(toDecimal, 10)


class YFOptionScrapperServiceBuilder:
    def __init__(self):
        self._instance = None

    def __call__(self):
        self._instance = YFOptionScrapperService("KeyValue1", "KeyValue2")
        return self._instance

    def authorize(self, key, secret):
        return 'PANDORA_CONSUMER_KEY', 'PANDORA_CONSUMER_SECRET'
