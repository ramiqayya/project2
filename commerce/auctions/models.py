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
    image = models.URLField(blank=True)
    time = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=64, default="Unspecified!")

    def __str__(self) -> str:
        return f"{self.title} by {self.seller}"


class Bid(models.Model):
    bidder = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="buyer")
    bid = models.PositiveIntegerField()
    listing = models.ForeignKey(Auction_Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.bid} by {self.bidder} "


class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviewer")
    listing = models.ForeignKey(
        Auction_Listing, on_delete=models.CASCADE, related_name="comment")
    comment = models.TextField(max_length=250)

    def __str__(self) -> str:
        if self.listing.exists():
            return f"Comment by {self.user} on {self.listing.first()}"
        else:
            return f"Comment by {self.user} without a listing association"
