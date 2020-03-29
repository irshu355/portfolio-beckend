from __future__ import absolute_import, unicode_literals
import requests
from ticker.serializers import TickerSerializer
from ticker.models import Ticker
from rest_framework.views import APIView, Response
from django.http import Http404
from rest_framework import generics
from rest_framework import status


class DALManager:
    def __init__(self):
        self.urlStockManager = "http://127.0.0.1:8000/api/v1/stock-manager/"
        pass

    def postTicker(self, data):
        ticker = self.get_ticker_object(data["symbol"])
        if ticker == Http404:
            print("insert")
            serializer = TickerSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return data
            return "bad request, ticker worker failed to insert"
        else:
            serializer = TickerSerializer(ticker, data=data)
            if (serializer.is_valid()):
                serializer.save()
                return data
            return "bad request, ticker worker failed to update"

    def get_ticker_object(self, symbol):
        try:
            return Ticker.objects.get(symbol=symbol)
        except Ticker.DoesNotExist:
            return Http404

    def getTickers(self):
        return Ticker.objects.all()
