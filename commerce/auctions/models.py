from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    categoryName = models.CharField(max_length=100)
    
    def __str__(self):
        return self.categoryName
    

class Bids(models.Model):
    bid = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="userbids")
    
class Listing(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    imageUrl = models.CharField(max_length=1000)
    price = models.ForeignKey(Bids, on_delete=models.CASCADE, blank=True, null=True, related_name="newPrice")
    isActive = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="watchlist")
   
    def __str__(self):
        return self.title

class Comments(models.Model):
    commentator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="commentator")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="listingCommented")
    comment = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.commentator} commented on {self.listing}"
            