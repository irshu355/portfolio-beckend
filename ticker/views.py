from __future__ import absolute_import, unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework import permissions
from django.contrib.auth.models import User, Group
from ticker.models import Ticker, WatchList, Option, Symbol, UserProfile, QuoteWareHouse
from rest_framework.views import APIView, Response
from django.http import Http404
from rest_framework import generics
from rest_framework import status
import datetime
import ticker.serializers as ticker_serializers
from rest_framework.decorators import api_view
import json
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework.authtoken.models import Token
from workers.scrapperservice.dalmanager import DALManager
from workers.scrapperservice import main
import workers.tasks as worker_tasks
from django.http import QueryDict, JsonResponse
from django.db.models import Q
from dateutil import parser
from django.contrib.auth.decorators import login_required
from datetime import date, datetime, timedelta
from django.conf import settings


@api_view(['POST'])
@login_required
def toggleWatchlist(request):

    user = request.user

    symbol = QueryDict(request.body)['ticker']
    # token = request.headers['authorization'].split('Token ')[1]
    # user = Token.objects.get(key=token).user
    profile = UserProfile.objects.get(user__email=request.user.email)
    ticker = Ticker.objects.filter(symbol=symbol).first()
    watchItem = WatchList.objects.filter(
        ticker__symbol=symbol).filter(owner=profile).first()
    if ticker == None or watchItem == None:
        dalManager = DALManager()
        data = main._scrap(symbol)

        # try:
        #     return Ticker.objects.get(symbol=symbol)
        # except Ticker.DoesNotExist:
        #     return Http404

    if watchItem == None:
        ticker = Ticker.objects.filter(symbol=symbol).first()
        obj = WatchList.objects.create(ticker=ticker, owner=profile)
    else:
        watchItem.delete()
    return JsonResponse({'symbol': symbol, 'subscribed': 1 if watchItem == None else 0})


@api_view(['GET'])
def getWatchListByUserId(request):
    queryset = WatchList.objects.select_related('ticker').all()
    list = []
    for obj in queryset:
        list.append(obj.ticker)

    serializer = ticker_serializers.TickerSerializer(list, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def getSymbols(request):
    symbol = request.GET['symbol']

    user = request.user

    watchList = WatchList.objects.filter(owner__user=user)

    querySet = Symbol.objects.filter(
        symbol__startswith=symbol).order_by('symbol')

    list = []
    for rec in querySet:
        obj = {}
        obj["id"] = rec.id
        obj["symbol"] = rec.symbol
        obj["security_name"] = rec.security_name
        obj["exchange"] = rec.exchange
        subscribed = watchList.filter(
            ticker__symbol=rec.symbol).first()
        obj["subscribed"] = 0 if subscribed == None else 1
        list.append(obj)

    return JsonResponse(list, safe=False)


@api_view(['GET'])
def getOptionsByTicker(request):
    ticker = request.GET['ticker']
    querySet = Option.objects.filter(
        ticker__symbol=ticker)

    serializer = ticker_serializers.OptionsSerializer(querySet, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def getOptionsByExpiry(request):
    ticker = request.GET['symbol']
    expires = request.GET['expires']

    date_string = expires + ' 00:00:00'
    date_object = parser.parse(date_string)

    querySet = Option.objects.filter(
        Q(ticker__symbol=ticker) & Q(expires=date_object.date()))

    serializer = ticker_serializers.OptionsSerializer(querySet, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def getOptionsExpiries(request):
    ticker = request.GET['ticker']
    querySet = Option.objects.filter(ticker__symbol=ticker).distinct('expires')

    serializer = ticker_serializers.OptionsExpirySerializer(
        querySet, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def getOptionsWithIvByTicker(request):
    ticker = request.GET['ticker']
    querySet = Option.objects.filter(
        ticker__symbol=ticker).order_by('-iv')[:10]

    serializer = ticker_serializers.OptionsSerializer(querySet, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def getOptionsWithVolByTicker(request):
    ticker = request.GET['ticker']
    querySet = Option.objects.filter(
        ticker__symbol=ticker).order_by('-volume')[:10]

    serializer = ticker_serializers.OptionsSerializer(querySet, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def getTicker(request, symbol):
    print(symbol)


@api_view(['GET'])
def getHistoricalIntra(request):
    # 1D = 2Min
    # 5d(1W) = 5min
    # 1M = 3 hrs, 9.30,12.30,4.00pm
    # 6M = open and close
    # 1Y =  1D close
    # 5Y = 1W close

    interval = request.GET['interval']
    symbol = request.GET['symbol']

    now = datetime.now()

    marketOpens = todayAt(9, 30, 00)

    day = now.strftime("%A")

    if day == 'Saturday':
        now = marketOpens - timedelta(days=1)
    elif day == 'Sunday':
        now = marketOpens - timedelta(days=2)
    elif now < marketOpens:
        now = marketOpens - timedelta(
            days=3) if day == 'Monday' else marketOpens - timedelta(days=1)

    querySet = QuoteWareHouse.objects.filter(
        Q(symbol=symbol) & Q(timestamp__startswith=now.date()) & Q(interval=interval))

    if querySet.count() == 0:
        worker_tasks.scrapHistoricalQuotes.delay(
            symbol, settings.QUOTE_INTRA_DAY_DELAY)

        return Response([], status=status.HTTP_208_ALREADY_REPORTED)

    serializer = ticker_serializers.QuoteWarehouseSerializer(
        querySet, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
    # querySet = QuoteWareHouse.objects.get(symbol=symbol).


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
            serializer = ticker_serializers.TickerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = ticker_serializers.TickerSerializer(
                ticker, data=request.data)
            if (serializer.is_valid()):
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TickerViewSet(viewsets.ModelViewSet):
    serializer_class = ticker_serializers.TickerSerializer
    queryset = Ticker.objects.all()
    # permission_classes = [permissions.IsAuthenticated]


class ListTickerView(generics.ListAPIView):
    """
    Provides a get method handler.
    """

    queryset = Ticker.objects.all()
    serializer_class = ticker_serializers.TickerSerializer


def todayAt(hr, min=0, sec=0):
    now = datetime.now()
    return now.replace(hour=hr, minute=min, second=sec)


# Create your views here.
