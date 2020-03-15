from workers.scrapperservice.factory.scrapperobjectfactory import ScrapperObjectFactory
from workers.scrapperservice.factory.nasdaq import nasdaqscrapper
from workers.scrapperservice.factory.cnbc import cnbcscrapper


class Scrapper:
    def __init__(self):
        self.factory = ScrapperObjectFactory()
        self.factory.register_builder(
            "NASDAQ", nasdaqscrapper.NasdaqScrapperServiceBuilder())
        self.factory.register_builder(
            "CNBC", cnbcscrapper.CNBCScrapperServiceBuilder())
