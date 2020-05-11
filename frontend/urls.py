from django.conf.urls import url
from . import views
from .views import CustomAuthToken
from django.urls import include, path, re_path
urlpatterns = [
    url(r'^$', views.index, name='index'),
    path('chat/<str:room_name>/', views.room, name='room'),
    url(r'^user/api-token-auth/', CustomAuthToken.as_view())
]
