from workers.scrapperservice.factory.scrapper import Scrapper
from workers.scrapperservice.dalmanager import DALManager

# stock quotes


def scrap(ticker):
    x = Scrapper()
    dal = DALManager()
    tickerInstance = x.getScrapper()
    data = tickerInstance().scrapTicker(ticker)
    result = dal.postTicker(data)
    return result


def scrapAll():
    scrapper = Scrapper()
    dal = DALManager()
    list = dal.getTickers()
    tickerInstance = scrapper.getScrapper()
    for t in list:
        data = tickerInstance().scrapTicker(t)
        dal.postTicker(data)
    return "ok"


# stock options

def _scrapOption(ticker):
    x = Scrapper()
    dal = DALManager()
    optionInstance = x.getScrapperOption()
    contracts = optionInstance().scrapOption(ticker)
    print(contracts)
