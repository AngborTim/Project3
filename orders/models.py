from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.utils import timezone
from django.db.models import Sum

import random

def TMP_ID():
    tmpid = str(random.random())[3:10];
    return tmpid

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    userTempId = models.CharField(max_length=64, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class ItemType(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class Item(models.Model):
    itemtype = models.ForeignKey(ItemType, on_delete=models.CASCADE, related_name="itemtype")
    name = models.CharField(max_length=64)
    has_extra_toppings = models.IntegerField(default=0)
    priceSmall = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    priceLarge = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.itemtype} {self.name} {self.has_extra_toppings} {self.priceSmall} {self.priceLarge}"

class Topping(models.Model):
    itemtype = models.ForeignKey(ItemType, on_delete=models.CASCADE, related_name="toppingtype")
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.itemtype} {self.name} {self.price}"

    def serializeCustom(self):
        data = {
            "itemtype": self.itemtype.name,
            "name": self.name,
            "price": self.price,
            }
        return data

class Size(models.Model):
    sizeName = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.sizeName}"

class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="item")
    topping = models.ManyToManyField(Topping, blank=True, related_name="topping")
    itemPrice = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    itemSize = models.ForeignKey(Size, on_delete=models.CASCADE, related_name="size")
    user_id = models.CharField(max_length=64)
    order_id = models.ForeignKey('Order', on_delete=models.CASCADE, related_name="order")

    def __str__(self):
        return f"{self.pk} ORDER: {self.order_id} {self.item} {self.topping} {self.itemPrice} {self.itemSize} {self.user_id} "

class OrderStatus(models.Model):
    orderType = models.CharField(max_length=64)
    def __str__(self):

        return f"{self.orderType}"


class Order(models.Model):
    user_id = models.CharField(max_length=64)
    order_date = models.DateTimeField(default=timezone.now, blank=True)
    order_id = models.CharField(max_length=64, default=TMP_ID())
    order_status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE, related_name="order_s", default=1)
    orderitem = models.ManyToManyField(OrderItem,  blank=True, related_name="items")
    total = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self):
        return f"User: {self.user_id}, order ID: {self.order_id}, status: {self.order_status}, order date: {self.order_date}, total: {self.total}"
