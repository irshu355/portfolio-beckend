from django.contrib import admin
from .models import Ticker, WatchList, UserProfile, Option, Symbol, Health, QuoteWareHouse

admin.site.register(UserProfile)
admin.site.register(Ticker)
admin.site.register(WatchList)
admin.site.register(Option)
admin.site.register(Symbol)
admin.site.register(QuoteWareHouse)
admin.site.register(Health)

# Register your models here.
