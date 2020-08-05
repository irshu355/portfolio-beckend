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
from datetime import date, datetime, timedelta, timezone
from django.conf import settings
import ticker.utils.utils as tickerUtils
import ticker.utils.dateutils as dateUtils
import pytz
from django.utils.timezone import localtime


@api_view(['POST'])
# @login_required
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
        data = main._addTicker(symbol)

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
def getSymbols(request, *args, **kwargs):
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
def getOptionsWithOpenInterestByTicker(request):
    ticker = request.GET['ticker']
    querySet = Option.objects.filter(
        ticker__symbol=ticker).order_by('-open_interest')[:20]

    for rec in querySet:
        print(rec.open_interest)

    serializer = ticker_serializers.OptionsSerializer(querySet, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def getOptionsWithVolByTicker(request):
    ticker = request.GET['ticker']
    querySet = Option.objects.filter(
        ticker__symbol=ticker).order_by('-volume')[:20]

    serializer = ticker_serializers.OptionsSerializer(querySet, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def getTicker(request, symbol):
    print(symbol)


@api_view(['GET'])
def historical_by_date_range(request):
    duration = request.GET['duration']
    symbol = request.GET['symbol']
    df = request.GET['from']
    dt = request.GET['to']

    date_from = datetime.strptime(df, '%Y%m%d%H%M%S')
    date_to = datetime.strptime(dt, '%Y%m%d%H%M%S')
    period, deltaD = tickerUtils.getPeriodTimeDelta(duration)

    server_timezone = pytz.timezone("America/New_York")
    aware_start_time = server_timezone.localize(date_from)  # aware object
    aware_end_time = server_timezone.localize(date_to)

    querySet = QuoteWareHouse.objects.filter(Q(symbol=symbol) & Q(
        timestamp__range=[aware_start_time, aware_end_time]) & Q(period=period)).order_by('timestamp')

    if querySet.count() == 0:
        worker_tasks.scrapHistoricalQuotesFromTo(
            symbol=symbol, duration=duration, date_from=df, date_to=dt)
        return HttpResponse(status=208)

    serializer = ticker_serializers.QuoteWarehouseSerializer(
        querySet, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def getHistorical(request):
    # 1D = 1M
    # 5d(1W) = 5M
    # 1M = 1H
    # 6M = 1D
    # 1Y =  1D
    # 5Y = 1W

    duration = request.GET['duration']
    symbol = request.GET['symbol']

    now = datetime.now()

    marketOpens = todayAt(9, 30, 00)
    marketClose = todayAt(15, 59, 59)

    # this only applies to periods not 1D
    if (now > marketClose):
        dateEnds = marketClose
    else:
        dateEnds = marketClose - timedelta(days=1)

    day = now.strftime("%A")

    # remember, we only need the date, so timezone doesnt really matter
    if day == 'Saturday':
        now = marketOpens - timedelta(days=1)
    elif day == 'Sunday':
        now = marketOpens - timedelta(days=2)
    elif now < marketOpens:
        now = marketOpens - timedelta(
            days=3) if day == 'Monday' else marketOpens - timedelta(days=1)
    else:
        # this is meant for 5D,1M,6M and 1Y to verify if historical needs to be loeaded from remote service
        backupNow = now - timedelta(days=1)

    try:
        backupNow
    except NameError:
        backupNow = now

    # if period 5D,1H,1D,1W or 1Y,
    period, deltaD = tickerUtils.getPeriodTimeDelta(duration)

    if deltaD != 0:
        now = dateUtils.date_by_adding_business_days(now, -1 * deltaD)

    if duration == '1D':
        querySet = QuoteWareHouse.objects.filter(Q(symbol=symbol) & Q(
            timestamp__startswith=now.date()) & Q(period=period)).order_by('timestamp')
    else:
        querySet = QuoteWareHouse.objects.filter(Q(symbol=symbol) & Q(
            timestamp__range=[now, dateEnds]) & Q(period=period)).order_by('timestamp')

    if querySet.count() == 0:
        worker_tasks.scrapHistoricalQuotes.delay(
            symbol, duration)

        return HttpResponse(status=208)

    # check if last record is yesterday for periods 5D,1M,6M,1Y
    if duration == '5D' or duration == '1M' or duration == '6M' or duration == '1Y':
        last = querySet[len(querySet) - 1] if querySet else None
        server_timezone = pytz.timezone("America/New_York")

        # one way to localize/timezoneaware a datetime object
        expectedLast = server_timezone.localize(backupNow)

        # django built-in way to localize/timezoneaware a datetime object
        actualLast = localtime(last.timestamp)

        #delta = expectedLast - last.timestamp
        if actualLast.day < expectedLast.day:
            worker_tasks.scrapHistoricalQuotes.delay(
                symbol, duration)
            return HttpResponse(status=208)
            # lastTime = last.timestamp.strftime("%y%m%d")
            # expectedTime = expectedLast.strftime("%y%m%d")

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
