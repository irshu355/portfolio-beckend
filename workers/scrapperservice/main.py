from workers.scrapperservice.factory.scrapper import Scrapper

config = {
    'spotify_client_key': 'THE_SPOTIFY_CLIENT_KEY',
    'spotify_client_secret': 'THE_SPOTIFY_CLIENT_SECRET',
    'pandora_client_key': 'THE_PANDORA_CLIENT_KEY',
    'pandora_client_secret': 'THE_PANDORA_CLIENT_SECRET',
    'local_music_location': '/usr/data/music'
}


def scrap(ticker):

    x = Scrapper()

    pandora = x.factory.create(
        "NASDAQ", **config)
    xx = pandora.scrapTicker(ticker)
    # dal.postTicker(ticker)
    return xx
