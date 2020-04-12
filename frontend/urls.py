from django.conf.urls import url
from . import views
from .views import CustomAuthToken

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^user/api-token-auth/', CustomAuthToken.as_view())
]
