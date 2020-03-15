from __future__ import absolute_import, unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework import permissions
from django.contrib.auth.models import User, Group
from ticker.serializers import TickerSerializer
from ticker.models import Ticker
from rest_framework.views import APIView, Response
from ticker.tasks import *

from rest_framework import generics


class CustomView(APIView):
    def get(self, request, *args, **kwargs):
        add.delay(10, 20)
        return Response("Some Get Response")

    def post(self, request, format=None):
        return Response("Some Post Response")


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


# Create your views here.
