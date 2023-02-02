from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Auction_Listing(models.Model):
    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listed_by")
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=500)
    starting_bid = models.PositiveIntegerField()
    image = models.URLField(required=False)


class Bid(models.Model):
    bidder = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="buyer")
    bid = models.PositiveIntegerField()
    listing = models.ForeignKey(Auction_Listing)
