from __future__ import absolute_import, unicode_literals
import requests
from ticker.serializers import TickerSerializer, OptionsSerializer, SymbolsSerializer
from ticker.models import Ticker, Option, WatchList, Symbol, Health, QuoteWareHouse
from rest_framework.views import APIView, Response
from django.http import Http404
from rest_framework import generics
from rest_framework import status
from workers.models import UpdateError
import pandas


class DALManager:
    def __init__(self):
        pass

    def reportFaultySource(self, _name, _status, _reason):
        Health.objects.create(name=_name, status=_status, reason=_reason)

    def postSymbols(self, data):
        for rec in data:
            single = self.get_symbol_object(rec["symbol"])
            if (single == Http404):
                serializer = SymbolsSerializer(data=rec)
            else:
                serializer = SymbolsSerializer(single, data=rec)
            if serializer.is_valid():
                print("adding " + rec["symbol"])
                serializer.save()
            else:
                return UpdateError("failed to insert/update symbol")

    def postOptions(self, data):
        symbol = ''
        tickerId = 0
        for contract in data:
            single = self.get_option_object(
                contract["contract_name"], contract["contract_name"])

            if symbol != contract["symbol"]:
                ticker = self.get_ticker_object(contract["symbol"])
                symbol = contract["symbol"]
                tickerId = ticker.id
                contract["ticker"] = ticker.id
            else:
                contract["ticker"] = tickerId
            if single == Http404:
                serializer = OptionsSerializer(data=contract)
            else:
                serializer = OptionsSerializer(single, data=contract)

            if serializer.is_valid():
                print("adding " + contract["contract_name"])
                serializer.save()
            else:
                return UpdateError("failed to insert/update option")

    def postTicker(self, data):
        ticker = self.get_ticker_object(data["symbol"])
        if ticker == Http404:
            serializer = TickerSerializer(data=data)
        else:
            serializer = TickerSerializer(ticker, data=data)
        if serializer.is_valid():
            print("updating" + data["symbol"] + "via " + data["source"])
            serializer.save()
            return data
        return "bad request, ticker worker failed to insert/update"

    def get_ticker_object(self, symbol):
        try:
            return Ticker.objects.get(symbol=symbol)
        except Ticker.DoesNotExist:
            return Http404

    def getTickers(self):
        return Ticker.objects.all()

    def getWatchList(self):
        list = WatchList.objects.filter(owner__is_online=1).distinct('ticker')
        arr = []
        for rec in list:
            arr.append(rec)
        arr.sort(key=lambda x: x.ticker.symbol)
        return arr
        #x=WatchList.objects.filter(owner__tier=1) .distinct('ticker').values_list('ticker__symbol',flat=True)

    # options

    def get_option_object(self, symbol, contractName):
        try:
            return Option.objects.get(contract_name=contractName)
        except Option.DoesNotExist:
            return Http404

    def get_symbol_object(self, symbol):
        try:
            return Symbol.objects.get(symbol=symbol)
        except Symbol.DoesNotExist:
            return Http404

    # historical data

    def postQuoteHistorical(self, history):
        symbol = ''
        tickerId = 0
        forInsert = []
        for rec in history:
            if symbol != rec["symbol"]:
                ticker = self.get_ticker_object(rec["symbol"])
                symbol = rec["symbol"]
                tickerId = ticker.id
                rec["ticker"] = ticker.id
            else:
                rec["ticker"] = tickerId

            exists = self.get_historical_object(
                rec["ticker"], rec["timestamp"])

            if (exists == Http404):
                forInsert.append(QuoteWareHouse(
                    ticker=ticker, open=rec["open"], close=rec["close"], high=rec["high"], low=rec["low"],
                    timestamp=rec["timestamp"], volume=rec["volume"], symbol=rec["symbol"]))

        QuoteWareHouse.objects.bulk_create(forInsert)

    def get_historical_object(self, ticker, timestamp):
        try:
            return QuoteWareHouse.objects.get(ticker=ticker, timestamp=timestamp)
        except QuoteWareHouse.DoesNotExist:
            return Http404
