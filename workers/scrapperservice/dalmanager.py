from __future__ import absolute_import, unicode_literals
import requests
from ticker.serializers import TickerSerializer, OptionsSerializer, SymbolsSerializer
from ticker.models import Ticker, Option, WatchList, Symbol
from rest_framework.views import APIView, Response
from django.http import Http404
from rest_framework import generics
from rest_framework import status
from workers.models import UpdateError
import pandas


class DALManager:
    def __init__(self):
        self.urlStockManager = "http://127.0.0.1:8000/api/v1/stock-manager/"
        pass

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

        for contract in data:
            single = self.get_option_object(
                contract["contract_name"], contract["contract_name"])
            ticker = self.get_ticker_object(contract["symbol"])
            contract["ticker"] = ticker.id
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
            print("adding" + data["symbol"])
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
        return WatchList.objects.all()

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
