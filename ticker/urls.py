from django.urls import include, path
from ticker.views import ListTickerView, index

urlpatterns = [
    path('stock-manager/', include('rest_framework.urls', namespace='rest_framework')),
    path('tickers/', ListTickerView.as_view(), name="tickers-all")
]
