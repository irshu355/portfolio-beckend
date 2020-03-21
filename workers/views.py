from __future__ import absolute_import, unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
import datetime
from workers.tasks import scrapTicker, add
from ticker.models import Ticker

# Create your tasks here
from celery import shared_task
from workers.scrapperservice.main import scrap
from ticker.views import CustomView
from django.http import Http404
from rest_framework import status
from ticker.serializers import TickerSerializer
from rest_framework.views import APIView, Response


def get_date(request):
    now = datetime.datetime.now()
    scrapTicker.delay('AAPL')
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)
