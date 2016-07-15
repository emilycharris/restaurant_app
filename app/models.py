from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save



# Create your models here.

class Position(models.Model):
    position = models.CharField(max_length=20)

    def __str__(self):
        return self.position

class Profile(models.Model):
    user = models.OneToOneField('auth.User')
    position = models.ForeignKey(Position, null=True, blank=True)

class Category(models.Model):
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.category

class Menu(models.Model):
    user = models.ForeignKey('auth.User')
    item = models.CharField(max_length=50)
    description = models.TextField()
    category = models.ForeignKey(Category)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField(upload_to="item_photos", null=True, blank=True)

    def __str__(self):
        return self.item

    @property
    def photo_url(self):
        if self.photo:
            return self.photo.url


class Order(models.Model):
    server = models.ForeignKey('auth.User')
    created = created = models.DateTimeField(auto_now_add=True)
    fulfilled = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

class Items(models.Model):
    order_id = models.ForeignKey(Order)
    item = models.ForeignKey(Menu, blank=True, null=True)
    quantity = models.PositiveSmallIntegerField(blank=True, null=True)
    notes = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return str(self.order_id)

@receiver(post_save, sender='auth.User')
def create_user_profile(**kwargs):
    created = kwargs.get("created")
    instance = kwargs.get("instance")
    if created:
        Profile.objects.create(user=instance)
