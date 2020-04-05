from django.contrib import admin
from .models import Ticker, WatchList, UserProfile, Option, Symbol

admin.site.register(UserProfile)
admin.site.register(Ticker)
admin.site.register(WatchList)
admin.site.register(Option)
admin.site.register(Symbol)

# Register your models here.
