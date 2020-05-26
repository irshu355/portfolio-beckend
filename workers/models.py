from django.db import models
from enum import Enum


class TickerScrapperSource(Enum):
    NASDAQ = "NASDAQ_QUOTES"
    CNBC = "CNBC_QUOTES"
    YF = "YF_QUOTES"


class OptionsScrapperSource(Enum):
    Zachs = "ZACHS_OPTIONS"
    YF = "YF_OPTIONS"


class HistoricalQuoteScrapperSource(Enum):
    AlphaVintage = "ALPHA_VINTAGE"
    CNBC = "CNBC"


class UpdateError:

    def __Init__(self, error):
        self.error = error

        # Create your models here.
