from django.db import models

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=100)
    product_price = models.IntegerField(default=0)
    out_of_stock = models.BooleanField(default=False)
    category = models.CharField(max_length=100)
    product_image = models.CharField(max_length=100)

class Cart(models.Model):
    product_name = models.CharField(max_length=100)
    total_price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    product_image = models.CharField(max_length=100)
    product_price = models.IntegerField(default=0)