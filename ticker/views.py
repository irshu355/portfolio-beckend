from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework import permissions
from django.contrib.auth.models import User, Group
from ticker.serializers import TickerSerializer
from ticker.models import Ticker


from rest_framework import generics





class TickerViewSet(viewsets.ModelViewSet):
    serializer_class = TickerSerializer
    queryset = Ticker.objects.all()
    #permission_classes = [permissions.IsAuthenticated]

class ListTickerView(generics.ListAPIView):
    """
    Provides a get method handler.
    """

    queryset = Ticker.objects.all()
    serializer_class = TickerSerializer

def index(request):
        return HttpResponse("Hello, world. You're at the polls index.")









# Create your views here.
