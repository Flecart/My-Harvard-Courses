from django.contrib import admin
from .models import *

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "title", "current_bid")


class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "current_bidder", "highest_bid", "listing")


class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "listing", "content")


# Register your models here.
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Watchlist)
admin.site.register(Category)
admin.site.register(ListingCategory)
admin.site.register(User)