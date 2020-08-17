from django.urls import include, path
from ticker import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'stocks-manager', views.TickerViewSet)


urlpatterns = [

    path('tickers/', views.ListTickerView.as_view(), name="tickers-all"),
    path(r'stocks', views.TickerApi.as_view()),
    path(r'watchlist_by_userid', views.getWatchListByUserId),
    path(r'option_expiries_by_ticker', views.getOptionsExpiries),
    path(r'options_by_ticker', views.getOptionsByTicker),
    path(r'options_by_expiry', views.getOptionsByExpiry),
    path(r'option_statistics_by_ticker', views.getOptionStatistics),
    path(r'options_with_oi_by_ticker', views.getOptionsWithOpenInterestByTicker),
    path(r'options_with_vol_by_ticker', views.getOptionsWithVolByTicker),
    path(r'toggle_watchlist', views.toggleWatchlist),
    path(r'symbols', views.getSymbols),
    path(r'ticker/<str:symbol>', views.getTicker),
    path(r'historical', views.getHistorical),
    path(r'historical_by_date_range', views.historical_by_date_range)
]

urlpatterns += router.urls
