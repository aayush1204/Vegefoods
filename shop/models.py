from django.db import models

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=100)
    product_price = models.IntegerField(default=0)
    out_of_stock = models.BooleanField(default=False)
    category = models.CharField(max_length=100)
    product_image = models.CharField(max_length=100)
