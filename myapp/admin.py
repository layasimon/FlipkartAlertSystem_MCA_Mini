from django.contrib import admin
from . models import LoginUser
from . models import HomeUser
from . models import WatchlistItem
from . models import WatchlistHistory


# Register your models here.
admin.site.register(LoginUser)
admin.site.register(HomeUser)
admin.site.register(WatchlistItem)
admin.site.register(WatchlistHistory)



 

