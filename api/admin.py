from django.contrib import admin

# Register your models here.
from .models import (
    Category, Product, User, Order, OrderItem, Review, ShippingAddress
)

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(User)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Review)
admin.site.register(ShippingAddress)