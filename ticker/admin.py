from django.contrib import admin
from .models import Ticker, WatchList, UserProfile

admin.site.register(UserProfile)
admin.site.register(Ticker)
admin.site.register(WatchList)

# Register your models here.
