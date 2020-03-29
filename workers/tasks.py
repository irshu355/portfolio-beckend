# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from workers.scrapperservice.main import scrap, scrapAll, _scrapOption


@shared_task
def add(a, b):
    return a + b


@shared_task
def scrapTickers():
    return scrapAll()


@shared_task
def scrapTicker(ticker):
    return scrap(ticker)


@shared_task
def scrapOption(ticker):
    return _scrapOption(ticker)
