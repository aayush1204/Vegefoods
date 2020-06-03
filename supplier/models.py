from django.db import models
from django.conf import settings
#from django.utils import timezone


class Supplier(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)
    address = models.TextField()
    number = models.CharField(max_length=15)
    #address = models.TextField()
    pincode=models.PositiveIntegerField()
    GST_number=models.PositiveIntegerField()
    Bank_Account_Details=models.TextField()
    store_name = models.CharField(max_length=50)
    store_description = models.CharField(max_length=200)
    store_address=models.TextField()
#    product = ForeignKey

    #signature-will be an image

    username =models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    confirm_password = models.CharField(max_length=100)
    #data_created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username




class Product(models.Model):
     product_name = models.CharField(max_length=100)
     product_description = models.CharField(max_length=100)
     product_sku=models.IntegerField(default=1)
     product_price = models.IntegerField(default=0)
     out_of_stock = models.BooleanField(default=False)
     category = models.CharField(max_length=100)
     supplier=models.ForeignKey(Supplier, null=True, on_delete = models.SET_NULL)
    # product_image =

     def __str__(self):
         return self.product_name
