from django.urls import include, path
from ticker.views import ListTickerView, CustomView, TickerViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'stock-manager', TickerViewSet)


urlpatterns = [
    path('tickers/', ListTickerView.as_view(), name="tickers-all"),
    path(r'customview', CustomView.as_view()),
]

urlpatterns += router.urls
