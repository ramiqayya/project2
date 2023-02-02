from django.contrib import admin
from .models import User, Auction_Listing, Bid


# Register your models here.

admin.site.register(User)
admin.site.register(Auction_Listing)
admin.site.register(Bid)
