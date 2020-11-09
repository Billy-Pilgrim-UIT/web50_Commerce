from django.contrib.auth.models import AbstractUser
from django.db import models






class Category(models.Model):
    category = models.CharField(max_length=64)




class Listing(models.Model):

    # retrieving list of categories and storing in a list of tuples.
    categories = Category.objects.all()
    CATEGORY_CHOICES = []

    for category in categories:
        cat_tuple = (category.id, category.category)
        CATEGORY_CHOICES.append(cat_tuple)

    time_created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=2048)
    imageURL = models.URLField(max_length=2048, null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    num_bids = models.IntegerField(default=0)
    listed_by = models.CharField(max_length=64)
    category = models.CharField(
        max_length = 64,
        choices = CATEGORY_CHOICES,
        default = 999
    )

    def __str__(self):
        return f"{self.id}: {self.title} listed by {self.listed_by}"


class Bids(models.Model):
    time_bid = models.DateTimeField(auto_now_add=True)
    bid = models.DecimalField(max_digits=8, decimal_places=2)
    bidder = models.CharField(max_length=64)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)


class Comments(models.Model):
    time_commented = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
    commenter = models.CharField(max_length=64)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

class Watchlist(models.Model):
    user = models.CharField(max_length=64)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

class User(AbstractUser):
    pass