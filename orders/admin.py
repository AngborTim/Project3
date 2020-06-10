from django.contrib import admin

from .models import ItemType, Item, Toppings, Order, TmpOrder, OrderItem, Size


admin.site.register(ItemType)
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Toppings)
admin.site.register(TmpOrder)
admin.site.register(Size)
