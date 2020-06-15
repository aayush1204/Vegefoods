from django.db import models

# Create your models here.
class adminmodel(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)

class addproductlist(models.Model):
    # requestid = models.IntegerField(primary_key=True)
    # id=models.BigIntegerField(default=1,primary_key=True)
    product_name=models.CharField(max_length=100)
    product_description=models.CharField(max_length=100)
    product_sku=models.CharField(max_length=100)
    product_price=models.FloatField()
    supplier_username=models.CharField(max_length=100)
    is_approved=models.BooleanField(default=False)

class delete_product_list(models.Model):
    product_name=models.CharField(max_length=100)
    product_description=models.CharField(max_length=100)
    product_sku=models.CharField(max_length=100)
    product_price=models.FloatField()
    reason_for_removal=models.TextField(default="")
    supplier_username=models.CharField(max_length=100)
    is_approved=models.BooleanField(default=False)
