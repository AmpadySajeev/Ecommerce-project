from django.contrib import admin
from .models import Category, Shoes, ShoeImage, Cart, Order, OrderItem

# Register your models here.

admin.site.register(Category)
admin.site.register(Shoes)
admin.site.register(ShoeImage)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)