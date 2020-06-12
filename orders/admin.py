from django.contrib import admin

from .models import ItemType, Item, Topping, Order, OrderItem, Size, Profile, OrderStatus

admin.site.register(Profile)

admin.site.register(ItemType)
admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Topping)
admin.site.register(Order)
admin.site.register(OrderStatus)
admin.site.register(Size)
