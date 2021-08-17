from django.contrib.auth.models import AbstractUser
from django.db import models
from .globals import *

class User(AbstractUser):
    pass


class Listing(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing_author")
    title = models.CharField(max_length=MAX_LISTING_LEN)
    description = models.CharField(max_length=MAX_DESCRIPTION_LEN)
    current_bid = models.IntegerField()
    image_link = models.CharField(max_length=MAX_DESCRIPTION_LEN, default="https://i.imgur.com/5G2zYum.png")
    closed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.id}: {self.title}"
    

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist_user")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watchlist_listing")

    def __str__(self) -> str:
        return f"{self.user} - {self.listing}"


class Category(models.Model):
    name = models.CharField(max_length=MAX_CATEGORY_LEN)

    def __str__(self) -> str:
        return f"{self.name}"


class ListingCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="category_listing")

    def __str__(self) -> str:
        return f"{self.listing} - {self.category}"


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids_listings")
    current_bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    highest_bid = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.id}: {self.current_bidder} in {self.listing} for {self.highest_bid}"


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_author")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comment_listings")
    content = models.CharField(max_length=MAX_COMMENT_LEN)

    def __str__(self) -> str:
        return f"{self.id}: {self.author} in {self.listing}"