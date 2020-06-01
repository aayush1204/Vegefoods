from django.contrib import admin

# Register your models here.

from .models import Product ,Supplier, Cart, Address , Order , ContactUs

admin.site.register(Supplier)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(ContactUs)

