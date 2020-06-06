# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from ticker.utils.utils import UserTier
from decimal import Decimal


class Health(models.Model):
    name = models.CharField(
        unique=True, max_length=30, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    reason = models.CharField(
        unique=False, max_length=500, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + "("+str(self.status)+") ->" + self.reason

    class Meta:
        managed = True
        db_table = 'health'


class Symbol(models.Model):
    symbol = models.CharField(
        unique=True, max_length=30, blank=True, null=True)
    security_name = models.CharField(
        max_length=300, blank=True, null=True)
    exchange = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(default=now, editable=False)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.symbol + " - "+self.security_name

    class Meta:
        managed = True
        db_table = 'symbols'


class Ticker(models.Model):
    symbol = models.CharField(
        unique=True, max_length=30, blank=True, null=True)
    price = models.DecimalField(
        max_digits=20, decimal_places=10, blank=True, null=True)
    name = models.CharField(unique=True, max_length=80, blank=True, null=True)
    sector = models.CharField(
        unique=False, max_length=90, blank=True, null=True)
    industry = models.CharField(
        unique=False, max_length=90, blank=True, null=True)

    previous_close = models.DecimalField(
        max_digits=20, decimal_places=10, blank=True, null=True)

    fifty_two_week_low = models.DecimalField(
        max_digits=20, decimal_places=10, blank=True, null=True)
    fifty_two_week_high = models.DecimalField(
        max_digits=20, decimal_places=10, blank=True, null=True)

    day_low = models.DecimalField(
        max_digits=20, decimal_places=10, blank=True, null=True)
    day_high = models.DecimalField(
        max_digits=20, decimal_places=10, blank=True, null=True)

    volume = models.IntegerField(blank=True, null=True)

    pe_ratio = models.DecimalField(
        max_digits=20, decimal_places=10, blank=True, null=True)
    eps = models.DecimalField(
        max_digits=20, decimal_places=10, blank=True, null=True)
    market_cap = models.BigIntegerField(blank=True, null=True)

    y1target = models.DecimalField(
        max_digits=20, decimal_places=10, blank=True, null=True)

    ninety_day_avg_volume = models.IntegerField(blank=True, null=True)

    forwardpe_one_year = models.DecimalField(
        max_digits=20, decimal_places=10, blank=True, null=True)

    annual_divident = models.DecimalField(
        max_digits=20, decimal_places=10, blank=True, null=True)

    ex_divident_date = models.CharField(
        unique=False, max_length=100, blank=True, null=True)

    exchange = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(default=now, editable=False)
    updated = models.DateTimeField(auto_now=True)
    source = models.CharField(
        unique=False, max_length=100, blank=True, null=True)

    def __str__(self):
        return self.symbol

    class Meta:
        managed = True
        db_table = 'tickers'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tier = models.IntegerField(
        choices=UserTier.choices(), default=UserTier.NORMAL)
    is_online = models.IntegerField(default=0)

    def get_user_tier(self):
        return UserTier(self.tier).name.title()

    def __str__(self):
        return self.user.email + " => "+self.get_user_tier()

    class Meta:
        managed = True
        db_table = 'user_profiles'

    # tier 99 => normal user, 100 =>Premium user, 101


class WatchList(models.Model):
    owner = models.ForeignKey(UserProfile,
                              on_delete=models.CASCADE)
    created = models.DateTimeField(default=now, editable=False)
    updated = models.DateTimeField(auto_now=True)
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    subscribe_options = models.IntegerField(default=0)

    def __str__(self):
        return self.owner.user.email + " => "+self.ticker.symbol

    class Meta:
        managed = True
        db_table = 'watch_lists'


class Option(models.Model):
    contract_name = models.CharField(
        unique=True, max_length=100, blank=False, null=False)

    ticker = models.ForeignKey(Ticker,
                               on_delete=models.CASCADE, related_name='options')

    contract_type = models.CharField(
        unique=False, max_length=1, blank=False, null=False)
    strike = models.DecimalField(
        max_digits=20, decimal_places=10)
    iv = models.DecimalField(
        max_digits=20, decimal_places=10, default=Decimal('0.00'))
    change = models.DecimalField(
        max_digits=20, decimal_places=10, blank=True, null=True, default=Decimal('0.00'))
    volume = models.IntegerField(blank=True, null=True, default=0)
    ask = models.DecimalField(
        max_digits=20, decimal_places=10, default=Decimal('0.00'))
    bid = models.DecimalField(
        max_digits=20, decimal_places=10, default=Decimal('0.00'))
    last_price = models.DecimalField(
        max_digits=20, decimal_places=10, blank=True, null=True, default=Decimal('0.00'))

    open_interest = models.IntegerField(blank=True, null=True, default=0)

    last_trade_date = models.DateTimeField(blank=True, null=True,)

    expires = models.DateField(null=False, blank=False)
    created = models.DateTimeField(default=now, editable=False)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.contract_type + "->" + self.contract_name

    @property
    def symbol(self):
        return self.ticker.symbol

    class Meta:
        managed = True
        db_table = 'options'


class QuoteWareHouse(models.Model):
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    open = models.DecimalField(
        max_digits=20, decimal_places=10, blank=False, null=False)
    high = models.DecimalField(
        max_digits=20, decimal_places=10, blank=False, null=False)
    low = models.DecimalField(
        max_digits=20, decimal_places=10, blank=False, null=False)
    close = models.DecimalField(
        max_digits=20, decimal_places=10, blank=False, null=False)
    symbol = models.CharField(
        unique=False, max_length=30, blank=False, null=False)
    volume = models.IntegerField(blank=False, null=False)
    timestamp = models.DateTimeField()

    def __str__(self):
        return self.symbol + " => "+self.timestamp.strftime("%d %b %y - %H:%M:00") + " => " + str(self.close)

    class Meta:
        managed = True
        db_table = 'quotes_warehouse'
