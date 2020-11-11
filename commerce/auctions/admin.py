from django.contrib import admin
from .models import Category, Listing, Bid, Comment, Watchlist


class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "bidder", "bid", "listing", "time_bid")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "commenter", "listing", "time_commented")

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "listed_by", "time_created", "active")

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("user", "listing")


# Register your models here.
admin.site.register(Category)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
