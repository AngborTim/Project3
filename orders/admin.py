from django.contrib import admin

from .models import ItemType, Item, OrderItem, Toppings, Order, TmpOrder

admin.site.register(ItemType)
admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Toppings)
admin.site.register(Order)
admin.site.register(TmpOrder)
