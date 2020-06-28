# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
import workers.scrapperservice.main
from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule


@shared_task
def add(a, b):
    return a + b


@shared_task
def toggleMarketScrappers(enabled):
    periodic_task = PeriodicTask.objects.get(
        name='quote scrapper every 5 seconds')
    periodic_task.enabled = True if enabled == 'y' else False
    periodic_task.save()


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


##########################################################################################################
# Historical tasks
##########################################################################################################


@shared_task
def scrapHistoricalQuotes(symbol, duration):
    return workers.scrapperservice.main._scrapHistoricalQuotes(symbol, duration)


@shared_task
def scrapHistoricalQuotesFromTo(symbol, duration, date_from, date_to):
    return workers.scrapperservice.main._scrapHistoricalQuotesFromTo(symbol, duration, date_from, date_to)
