from django.db import models
from enum import Enum


class TickerScrapperSource(Enum):
    NASDAQ = "NASDAQ"
    CNBC = "CNBC"


class OptionsScrapperSource(Enum):
    Zachs = "Zachs"
    YF = "YF"


class UpdateError:

    def __Init__(self, error):
        self.error = error

        # Create your models here.
