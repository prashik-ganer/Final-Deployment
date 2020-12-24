from django.contrib import admin
from . models import Customer, Product, Order, Tag, Seller
# Register your models here.

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Tag)
admin.site.register(Order)
admin.site.register(Seller)