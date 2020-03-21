# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


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
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.symbol

    class Meta:
        managed = True
        db_table = 'ticker'
