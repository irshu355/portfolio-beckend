from __future__ import absolute_import, unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
import datetime
from workers.tasks import scrapTicker


def get_date(request):
    now = datetime.datetime.now()
    scrapTicker.delay('MMM')
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)
