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


class Options(models.Model):
    contract_name = models.CharField(
        unique=True, max_length=100, blank=False, null=False)
    symbol = models.CharField(
        unique=False, max_length=30, blank=False, null=False)

    contract_type = models.CharField(
        unique=False, max_length=1, blank=False, null=False)
    strike = models.DecimalField(
        max_digits=8, decimal_places=2)
    iv = models.DecimalField(
        max_digits=10, decimal_places=2)
    change = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    volume = models.IntegerField(blank=True, null=True)
    ask = models.DecimalField(
        max_digits=8, decimal_places=2)
    bid = models.DecimalField(
        max_digits=8, decimal_places=2)
    last_price = models.DecimalField(
        max_digits=8, decimal_places=2, blank=False, null=False)

    created = models.DateTimeField(default=now, editable=False)
    updated = models.DateTimeField(auto_now=True)


class Ticker(models.Model):
    symbol = models.CharField(
        unique=True, max_length=30, blank=True, null=True)
    price = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)
    name = models.CharField(unique=True, max_length=80, blank=True, null=True)
    sector = models.CharField(
        unique=True, max_length=90, blank=True, null=True)
    industry = models.CharField(
        unique=True, max_length=90, blank=True, null=True)

    previous_close = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)

    fifty_two_week_low = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)
    fifty_two_week_high = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)

    day_low = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)
    day_high = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)

    volume = models.IntegerField(blank=True, null=True)
    pe_ratio = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True)
    eps = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True)
    market_cap = models.BigIntegerField(blank=True, null=True)

    exchange = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(default=now, editable=False)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.symbol

    class Meta:
        managed = True
        db_table = 'ticker'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tier = models.IntegerField(
        choices=UserTier.choices(), default=UserTier.NORMAL)

    def get_user_tier(self):
        return UserTier(self.tier).name.title()

    def __str__(self):
        return self.user.email + " => "+self.get_user_tier()

    class Meta:
        managed = True
        db_table = 'user_profile'

    # tier 99 => normal user, 100 =>Premium user, 101


class WatchList(models.Model):
    owner = models.ForeignKey(UserProfile,
                              on_delete=models.CASCADE)
    created = models.DateTimeField(default=now, editable=False)
    updated = models.DateTimeField(auto_now=True)
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)

    def __str__(self):
        return self.owner.user.email + " => "+self.ticker.symbol

    class Meta:
        managed = True
        db_table = 'watch_list'
