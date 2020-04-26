from rest_framework import serializers
from .models import *


class SymbolsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symbol
        fields = "__all__"


class TickerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticker
        fields = "__all__"


class WatchListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchList
        fields = "__all__"


class OptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = "__all__"


class OptionsExpirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['expires', 'id']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"
