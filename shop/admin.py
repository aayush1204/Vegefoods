from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.

from .models import Product, OrderSupplier ,Supplier, Cart, Address , Order , ContactUs, Profile, Society, Refunds

admin.site.register(Supplier)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(ContactUs)
admin.site.register(Refunds)
admin.site.register(Society)
admin.site.register(OrderSupplier)
admin.site.register(Profile)

class ProfileInline(admin.StackedInline):
    model=Profile
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline]

admin.site.unregister(User)

admin.site.register(User, UserAdmin)
