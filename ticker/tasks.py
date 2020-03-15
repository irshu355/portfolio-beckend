# Create your tasks here
from __future__ import absolute_import, unicode_literals

from celery import shared_task
from ticker.models import Ticker


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


@shared_task
def count_widgets():
    return 999


@shared_task
def rename_widget(widget_id, name):
    w = Widget.objects.get(id=widget_id)
    w.name = name
    w.save()
