# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
import workers.scrapperservice.main


@shared_task
def add(a, b):
    return a + b

##########################################################################################################
# Stock ticker quote tasks
##########################################################################################################


@shared_task
def scrapTicker(ticker):
    return workers.scrapperservice.main._scrap(ticker)


@shared_task
def scrapTickers():
    return workers.scrapperservice.main._scrapAll()


@shared_task
def scrapWatchListTickers():
    return workers.scrapperservice.main._scrapWatchListTickers()


##########################################################################################################
# Options tasks
##########################################################################################################


@shared_task
def scrapWatchOptions():
    return workers.scrapperservice.main._scrapWatchOptions()


@shared_task
def scrapOption(ticker):
    return workers.scrapperservice.main._scrapOption(ticker)


@shared_task
def scrapSymbolsNasdaq():
    return workers.scrapperservice.main._scrapSymbols(True)


@shared_task
def scrapSymbolsNYSE():
    return workers.scrapperservice.main._scrapSymbols(False)
