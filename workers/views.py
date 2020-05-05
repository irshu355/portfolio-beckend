from __future__ import absolute_import, unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
import datetime
from workers.tasks import scrapTicker, add, scrapTickers, scrapWatchOptions, scrapWatchListTickers, scrapOption, scrapSymbolsNasdaq, scrapSymbolsNYSE
from ticker.models import Ticker

# Create your tasks here
from celery import shared_task
from workers.scrapperservice.main import _scrap
from django.http import Http404, QueryDict, JsonResponse
from rest_framework import status
from ticker.serializers import TickerSerializer
from rest_framework.views import APIView, Response


def scrap_ticker(request):
    now = datetime.datetime.now()
    # scrapTicker.delay('AAPL')
    html = "<html><body>It is now %s.</body></html>" % now
    # return HttpResponse(html)

    scrapTicker(request.GET['symbol'])

    # scrapTickers.delay()
    return HttpResponse(html)


def scrap_watchlist_tickers(request):

    now = datetime.datetime.now()
    # scrapTicker.delay('AAPL')
    html = "<html><body>It is now %s.</body></html>" % now
    # return HttpResponse(html)

    scrapWatchListTickers()
    return HttpResponse(html)


def scrap_quote(request):
    now = datetime.datetime.now()
    # scrapTicker.delay('AAPL')
    html = "<html><body>It is now %s.</body></html>" % now
    # return HttpResponse(html)

    scrapTickers()

    # scrapTickers.delay()
    return HttpResponse(html)


def scrap_option(request):
    scrapOption(request.GET['symbol'])
    return JsonResponse({'status': 200})


def scrap_watchlist_options(request):
    scrapWatchOptions()
    return HttpResponse("html")


def scrap_symbols(request):
    type = request.GET['type']
    if (type == 'nasdaq'):
        scrapSymbolsNasdaq()
    else:
        scrapSymbolsNYSE()

    return HttpResponse("html")
