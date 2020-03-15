
from . import views
from django.urls import path

urlpatterns = [
    # ex: /polls/
    path('', views.get_date, name='index')
]
