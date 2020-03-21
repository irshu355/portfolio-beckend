# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from workers.scrapperservice.main import scrap


@shared_task
def add(a, b):
    return a+b


@shared_task
def scrapTicker(ticker):
    return scrap(ticker)
