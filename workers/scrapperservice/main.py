from workers.scrapperservice.factory.scrapper import Scrapper
from workers.scrapperservice.dalmanager import DALManager
import pandas as pd
import os
from django.conf import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from decimal import Decimal


##########################################################################################################
# Tickers scrapping
##########################################################################################################


def _scrapSymbols(nasdaqListed):
    symbols = []
    dal = DALManager()
    path = os.path.join(
        settings.BASE_DIR, 'nasdaqlisted.csv' if nasdaqListed else 'otherlisted.csv')

    data = pd.read_csv(path)
    for index, row in data.iterrows():
        if not nasdaqListed and row["Exchange"] != "N":
            continue

        obj = {}
        obj["symbol"] = row["Symbol"] if nasdaqListed else row["ACT Symbol"]
        obj["security_name"] = row["Security Name"]
        if nasdaqListed:
            obj["exchange"] = 0
        else:
            obj["exchange"] = 1
        symbols.append(obj)
    dal.postSymbols(symbols)
    pass


#
# stock quotes
#

def _scrap(ticker):
    x = Scrapper()
    dal = DALManager()
    tickerInstance = x.getScrapper()
    data = tickerInstance().scrapTicker(ticker)
    result = dal.postTicker(data)
    return result


def _scrapAll():
    scrapper = Scrapper()
    dal = DALManager()
    list = dal.getTickers()
    tickerInstance = scrapper.getScrapper()
    for t in list:
        data = tickerInstance().scrapTicker(t)
        dal.postTicker(data)
    return "ok"


def _scrapWatchListTickers():
    scrapper = Scrapper()
    dal = DALManager()
    list = dal.getWatchList()
    tickerInstance = scrapper.getScrapper()
    for watch in list:
        data = tickerInstance().scrapTicker(watch.ticker.symbol)
        transmitQuoteMessage(data)
        dal.postTicker(data)
    return "ok"


##########################################################################################################
    #Options scrapping#
##########################################################################################################


def _scrapWatchOptions():
    x = Scrapper()
    dal = DALManager()
    optionInstance = x.getScrapperOption()
    list = dal.getWatchList()
    for watch in list:
        contracts = optionInstance().scrapOption(watch.ticker.symbol)
        dal.postOptions(contracts)
        obj = {
            "symbol": watch.ticker.symbol
        }
        transmitOptionsRefreshMessage(obj)
    return "ok"


def _scrapOption(ticker):
    x = Scrapper()
    dal = DALManager()
    optionInstance = x.getScrapperOption()
    contracts = optionInstance().scrapOption(ticker)
    dal.postOptions(contracts)
    return "ok"


##########################################################################################################
    #Websocket#
##########################################################################################################

def transmitQuoteMessage(ticker):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        ticker["symbol"],
        {
            'type': 'quote_message',
            'message': ticker
        }
    )


def transmitOptionsRefreshMessage(data):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        data["symbol"],
        {
            'type': 'options_refresh_message',
            'message': data
        }
    )


##########################################################################################################
    #Tests#
##########################################################################################################

def streamTestTickerQuotes():
    dal = DALManager()
    list = dal.getWatchList()
    arr = []
    for x in list:
        obj = {
            "price": 120.00,
            "volume": 200,
            "symbol": x.ticker.symbol,
            "id": x.ticker.id
        }
        arr.append(obj)
        transmitQuoteMessage(obj)

    return arr
