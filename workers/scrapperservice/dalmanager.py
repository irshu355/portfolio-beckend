from __future__ import absolute_import, unicode_literals
import requests
from ticker.serializers import TickerSerializer, OptionsSerializer
from ticker.models import Ticker, Options, WatchList
from rest_framework.views import APIView, Response
from django.http import Http404
from rest_framework import generics
from rest_framework import status
from workers.models import UpdateError


class DALManager:
    def __init__(self):
        self.urlStockManager = "http://127.0.0.1:8000/api/v1/stock-manager/"
        pass

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
                print("valid")
                serializer.save()
            else:
                return UpdateError("failed to insert/update option")

    def postTicker(self, data):
        ticker = self.get_ticker_object(data["symbol"])
        if ticker == Http404:
            print("insert")
            serializer = TickerSerializer(data=data)
        else:
            serializer = TickerSerializer(ticker, data=data)
        if serializer.is_valid():
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
            return Options.objects.get(contract_name=contractName)
        except Options.DoesNotExist:
            return Http404
