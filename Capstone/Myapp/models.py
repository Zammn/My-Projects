from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    pass

class Recipe(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    imageUrl = models.CharField(max_length=1000, default=0)
    price = models.IntegerField(default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    directions = models.CharField(max_length=500, default=0)
    ingredients = models.CharField(max_length=300, default=0)
    
    class Meta:
        verbose_name = ("Recipe")
            
    def __str__(self):
        return self.title    