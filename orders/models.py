from django.db import models

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
    user_id = models.IntegerField(default=None)

    def __str__(self):
        return f"{self.user_id}"

class Toppings(models.Model):
    itemtype = models.ForeignKey(ItemType, on_delete=models.CASCADE, related_name="toppingtype")
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.itemtype} {self.name} {self.price}"


class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="item")
    toppings = models.ManyToManyField(Toppings, blank=True, related_name="toppings")
    itemPrice = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    itemSize = models.CharField(max_length=64)
    user_id = models.IntegerField(default=None)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order")

    def __str__(self):
        return f"{self.item} {self.has_toppings} {self.itemPrice} {self.itemSize} {self.user_id} {self.order_id}"
