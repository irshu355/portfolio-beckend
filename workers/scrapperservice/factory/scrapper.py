from workers.scrapperservice.factory.scrapperobjectfactory import ScrapperObjectFactory
from workers.scrapperservice.factory.stockquote.nasdaq import nasdaqscrapper
from workers.scrapperservice.factory.stockquote.cnbc import cnbcscrapper
from workers.scrapperservice.factory.stockquote.yahoofinance import yfinancescrapper
from workers.scrapperservice.factory.options.yahoofinance import yfoptionscrapper
from workers.models import TickerScrapperSource, OptionsScrapperSource
from ticker.models import Health


class Scrapper:
    def __init__(self):

        self.config = {
            'spotify_client_key': 'THE_SPOTIFY_CLIENT_KEY',
            'spotify_client_secret': 'THE_SPOTIFY_CLIENT_SECRET',
            'pandora_client_key': 'THE_PANDORA_CLIENT_KEY',
            'pandora_client_secret': 'THE_PANDORA_CLIENT_SECRET',
            'local_music_location': '/usr/data/music'
        }

        self.factory = ScrapperObjectFactory()
        # stock quote

        list = Health.objects.all()
        healths = []
        for rec in list:
            if rec.status == 200:
                continue
            healths.append(rec.name)

        # nasdaq quotes

        if not TickerScrapperSource.NASDAQ.value in healths:
            self.factory.register_builder(
                TickerScrapperSource.NASDAQ.value, nasdaqscrapper.NasdaqScrapperServiceBuilder())

        # yahoo finance  quotes
        if not TickerScrapperSource.YF.value in healths:
            self.factory.register_builder(
                TickerScrapperSource.YF.value, yfinancescrapper.YFinanceScrapperServiceBuilder())
        # self.factory.register_builder(
        #     "CNBC", cnbcscrapper.CNBCScrapperServiceBuilder())

        # options

        # yahoo finance  options
        if not OptionsScrapperSource.YF.value in healths:
            self.factory.register_options_builder(
                OptionsScrapperSource.YF.value, yfoptionscrapper.YFOptionScrapperServiceBuilder())

    def getScrapper(self):
        return self.factory.create(TickerScrapperSource.NASDAQ.value, **self.config)

    def getScrapperOption(self):
        return self.factory.createOption(OptionsScrapperSource.YF.value, **self.config)
