from django.contrib import admin
from .models import Ticker, WatchList, UserProfile, Options

admin.site.register(UserProfile)
admin.site.register(Ticker)
admin.site.register(WatchList)
admin.site.register(Options)

# Register your models here.
