from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Position(models.Model):
    position = models.CharField(max_length=20)

class Profile(models.Model):
    user = models.ForeignKey('auth.User')
    position = models.ForeignKey(Position)

class Category(models.Model):
    category = models.CharField(max_length=50)

class Menu(models.Model):
    item = models.CharField(max_length=50)
    description = models.TextField()
    category = models.ForeignKey(Category)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Order(models.Model):
    item = models.ForeignKey(Menu)
    quantity = models.IntegerField()
    notes = models.TextField()
    fulfilled = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
