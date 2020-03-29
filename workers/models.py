from django.db import models
from enum import Enum


class TickerScrapperSource(Enum):
    NASDAQ = "NASDAQ"
    CNBC = "CNBC"


class OptionsScrapperSource(Enum):
    Zachs = "Zachs"
    YF = "YF"

# Create your models here.
