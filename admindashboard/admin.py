from django.contrib import admin
from .models import adminmodel,addproductlist,delete_product_list
# Register your models here.
admin.site.register(adminmodel)
admin.site.register(addproductlist)
admin.site.register(delete_product_list)
