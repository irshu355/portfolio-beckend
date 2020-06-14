from __future__ import absolute_import, unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
import datetime
import workers.tasks
from ticker.models import Ticker
from django.conf import settings
# Create your tasks here
from celery import shared_task
from workers.scrapperservice.main import _scrap, streamTestTickerQuotes
from django.http import Http404, QueryDict, JsonResponse
from rest_framework import status
from ticker.serializers import TickerSerializer
from rest_framework.views import APIView, Response
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def scrap_ticker(request):
    now = datetime.datetime.now()
    # scrapTicker.delay('AAPL')
    html = "<html><body>It is now %s.</body></html>" % now
    # return HttpResponse(html)

    workers.tasks.scrapTicker(request.GET['symbol'])

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'BA',
        {
            'type': 'quote_message',
            'message': "event_trigered_from_views"
        }
    )

    # scrapTickers.delay()
    return HttpResponse(html)


def scrap_watchlist_tickers(request):

    now = datetime.datetime.now()
    # scrapTicker.delay('AAPL')
    html = "<html><body>It is now %s.</body></html>" % now
    # return HttpResponse(html)

    workers.tasks.scrapWatchListTickers()
    return HttpResponse(html)


def scrap_quote(request):
    now = datetime.datetime.now()
    # scrapTicker.delay('AAPL')
    html = "<html><body>It is now %s.</body></html>" % now
    # return HttpResponse(html)

    workers.tasks.scrapTickers()

    # scrapTickers.delay()
    return HttpResponse(html)


def scrap_option(request):
    workers.tasks.scrapOption(request.GET['symbol'])
    return JsonResponse({'status': 200})


def scrap_watchlist_options(request):
    workers.tasks.scrapWatchOptions()
    return HttpResponse("html")


def scrap_symbols(request):
    type = request.GET['type']
    if (type == 'nasdaq'):
        workers.tasks.scrapSymbolsNasdaq()
    else:
        workers.tasks.scrapSymbolsNYSE()

    return HttpResponse("OK")


def scrap_historical_quotes(request):
    workers.tasks.scrapHistoricalQuotes(
        request.GET['symbol'], request.GET['period'])
    return HttpResponse("OK")


# for running tests

def test_quote_sockets(request):
    list = streamTestTickerQuotes()
    return JsonResponse(list, safe=False)
