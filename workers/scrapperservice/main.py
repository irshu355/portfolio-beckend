from workers.scrapperservice.factory.scrapper import Scrapper
from workers.scrapperservice.dalmanager import DALManager


config = {
    'spotify_client_key': 'THE_SPOTIFY_CLIENT_KEY',
    'spotify_client_secret': 'THE_SPOTIFY_CLIENT_SECRET',
    'pandora_client_key': 'THE_PANDORA_CLIENT_KEY',
    'pandora_client_secret': 'THE_PANDORA_CLIENT_SECRET',
    'local_music_location': '/usr/data/music'
}


def scrap(ticker):
    x = Scrapper()
    dal = DALManager()
    pandora = x.factory.create("NASDAQ", **config)
    data = pandora.scrapTicker(ticker)
    result = dal.postTicker(data)
    return result
