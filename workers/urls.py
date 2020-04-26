
from . import views
from django.urls import path

urlpatterns = [
    # ex: /polls/
    path('', views.scrap_quote, name='index'),
    path('scrap-ticker', views.scrap_ticker, name='index'),
    path('scrap-option', views.scrap_option, name='option'),
    path('scrap-symbols', views.scrap_symbols, name='symbols'),
    path('scrap-watchlist-options',
         views.scrap_watchlist_options, name='options-watch-list')
]
