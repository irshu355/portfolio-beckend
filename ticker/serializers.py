from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ReadOnlyField
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
    symbol = ReadOnlyField(source='ticker.symbol')

    class Meta:
        model = Option
        fields = "__all__"


class OptionsExpirySerializer(serializers.ModelSerializer):
    symbol = serializers.ReadOnlyField()

    class Meta:
        model = Option
        fields = ['expires', 'id', 'symbol']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"


class QuoteWarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuoteWareHouse
        fields = ['timestamp', 'open', 'high', 'low', 'close', 'volume']


class QuoteWarehouseSerializerMinimal(serializers.ModelSerializer):
    class Meta:
        model = QuoteWareHouse
        fields = ['timestamp', 'close', 'volume']
