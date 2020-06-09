from django.db import models
from django.utils import timezone
from django.db.models import Sum
import random

def TMP_ID():
    tmpid = str(random.random())[3:8];
    return tmpid

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

class Order(models.Model):
    user_id = models.CharField(max_length=64)
    order_date = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return f"{self.user_id} {self.order_date}"

class Toppings(models.Model):
    itemtype = models.ForeignKey(ItemType, on_delete=models.CASCADE, related_name="toppingtype")
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.itemtype} {self.name} {self.price}"

class TmpOrder(models.Model):
    user_id = models.CharField(max_length=64)
    order_date = models.DateTimeField(default=timezone.now, blank=True)
    order_id = models.CharField(max_length=64, default=TMP_ID())
    total = OrderItem.objects.all().aggregate(Sum('itemPrice'))
    def __str__(self):
        return f"User: {self.user_id}, order ID: {self.order_id}, order date: {self.order_date}"

class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="item")
    toppings = models.ManyToManyField(Toppings, blank=True, related_name="toppings")
    itemPrice = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    itemSize = models.CharField(max_length=64)
    user_id = models.CharField(max_length=64)
    order_id = models.ForeignKey(TmpOrder, on_delete=models.CASCADE, related_name="order")

    def __str__(self):
        return f"ORDER: {self.order_id.order_id} {self.item} {self.toppings} {self.itemPrice} {self.itemSize} {self.user_id} "
