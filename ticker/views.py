from __future__ import absolute_import, unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework import permissions
from django.contrib.auth.models import User, Group
from ticker.serializers import TickerSerializer, WatchListSerializer, OptionsExpirySerializer, OptionsSerializer
from ticker.models import Ticker, WatchList, Option
from rest_framework.views import APIView, Response
from django.http import Http404
from rest_framework import generics
from rest_framework import status
import datetime
from rest_framework.decorators import api_view
import json
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder


@api_view(['GET'])
def getWatchListByUserId(request):
    queryset = WatchList.objects.select_related('ticker').all()
    list = []
    for obj in queryset:
        list.append(obj.ticker)

    serializer = TickerSerializer(list, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def getOptionsByTicker(request):
    ticker = request.GET['ticker']
    querySet = Option.objects.filter(
        ticker__symbol=ticker)

    serializer = OptionsSerializer(querySet, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def getOptionsByExpiry(request):
    ticker = request.GET['ticker']
    expires = request.GET['expires']
    querySet = Option.objects.filter(
        ticker__symbol=ticker).filter(expires=expires)

    serializer = OptionsSerializer(querySet, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def getOptionsExpiries(request):
    ticker = request.GET['ticker']
    querySet = Option.objects.values('expires').filter(
        ticker__symbol=ticker).distinct()

    serializer = OptionsExpirySerializer(querySet, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class TickerApi(APIView):

    def get_object(self, symbol):
        try:
            return Ticker.objects.get(symbol=symbol)
        except Ticker.DoesNotExist:
            return Http404

    def get(self, request, *args, **kwargs):
        now = datetime.datetime.now()
        html = "<html><body>It is now %s.</body></html>" % now
        return Response(html)

    def post(self, request, format=None):
        return Response("Some Post Response")

    def put(self, request, format=None):
        data = request.data
        ticker = self.get_object(data["symbol"])
        if ticker == Http404:
            print("insert")
            serializer = TickerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = TickerSerializer(ticker, data=request.data)
            if (serializer.is_valid()):
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TickerViewSet(viewsets.ModelViewSet):
    serializer_class = TickerSerializer
    queryset = Ticker.objects.all()
    # permission_classes = [permissions.IsAuthenticated]


class WatchListViewSet(viewsets.ModelViewSet):
    serializer_class = WatchListSerializer
    queryset = WatchList.objects.prefetch_related('ticker').all()
    # permission_classes = [permissions.IsAuthenticated]


class ListTickerView(generics.ListAPIView):
    """
    Provides a get method handler.
    """

    queryset = Ticker.objects.all()
    serializer_class = TickerSerializer


# Create your views here.
