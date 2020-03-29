
from . import views
from django.urls import path

urlpatterns = [
    # ex: /polls/
    path('', views.scrap_quote, name='index'),
    path('scrap-option', views.scrap_option, name='option')
]
