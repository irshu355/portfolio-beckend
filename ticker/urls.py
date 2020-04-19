from django.urls import include, path
from ticker.views import ListTickerView, TickerApi, TickerViewSet, WatchListViewSet, getWatchListByUserId, getOptionsExpiries, getOptionsByTicker, getOptionsByExpiry
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'stocks-manager', TickerViewSet)
router.register(r'watch-list-manager', WatchListViewSet)


urlpatterns = [
    path('tickers/', ListTickerView.as_view(), name="tickers-all"),
    path(r'stocks', TickerApi.as_view()),
    path(r'watchlist_by_userid', getWatchListByUserId),
    path(r'option_expiries_by_ticker', getOptionsExpiries),
    path(r'options_by_ticker', getOptionsByTicker),
    path(r'options_by_expiry', getOptionsByExpiry),
]

urlpatterns += router.urls
