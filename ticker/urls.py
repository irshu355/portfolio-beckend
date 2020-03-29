from django.urls import include, path
from ticker.views import ListTickerView, TickerApi, TickerViewSet, WatchListViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'stocks-manager', TickerViewSet)
router.register(r'watch-list-manager', WatchListViewSet)


urlpatterns = [
    path('tickers/', ListTickerView.as_view(), name="tickers-all"),
    path(r'stocks', TickerApi.as_view()),
]

urlpatterns += router.urls
