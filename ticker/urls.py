from django.urls import include, path
from ticker.views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'stocks-manager', TickerViewSet)


urlpatterns = [

    path('tickers/', ListTickerView.as_view(), name="tickers-all"),
    path(r'stocks', TickerApi.as_view()),
    path(r'watchlist_by_userid', getWatchListByUserId),
    path(r'option_expiries_by_ticker', getOptionsExpiries),
    path(r'options_by_ticker', getOptionsByTicker),
    path(r'options_by_expiry', getOptionsByExpiry),
    path(r'options_with_iv_by_ticker', getOptionsWithIvByTicker),
    path(r'options_with_vol_by_ticker', getOptionsWithVolByTicker),
    path(r'toggle_watchlist', toggleWatchlist),
    path(r'symbols', getSymbols),

]

urlpatterns += router.urls
