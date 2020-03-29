from workers.scrapperservice.factory.scrapper import Scrapper
from workers.scrapperservice.dalmanager import DALManager

# stock quotes


def _scrap(ticker):
    x = Scrapper()
    dal = DALManager()
    tickerInstance = x.getScrapper()
    data = tickerInstance().scrapTicker(ticker)
    result = dal.postTicker(data)
    return result


def _scrapAll():
    scrapper = Scrapper()
    dal = DALManager()
    list = dal.getTickers()
    tickerInstance = scrapper.getScrapper()
    for t in list:
        data = tickerInstance().scrapTicker(t)
        dal.postTicker(data)
    return "ok"


def _scrapWatchListTickers():
    scrapper = Scrapper()
    dal = DALManager()
    list = dal.getWatchList()
    tickerInstance = scrapper.getScrapper()
    for watch in list:
        data = tickerInstance().scrapTicker(watch.ticker.symbol)
        dal.postTicker(data)
    return "ok"


# stock options

def _scrapWatchOptions():
    x = Scrapper()
    dal = DALManager()
    optionInstance = x.getScrapperOption()
    list = dal.getWatchList()
    for watch in list:
        contracts = optionInstance().scrapOption(watch.ticker.symbol)
        dal.postOptions(contracts)
    return "ok"


def _scrapOption(ticker):
    x = Scrapper()
    dal = DALManager()
    optionInstance = x.getScrapperOption()
    contracts = optionInstance().scrapOption(ticker)
    dal.postOptions(contracts)
    return "ok"
