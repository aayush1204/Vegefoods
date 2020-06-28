from django.db import models
from shop.models import Supplier

# Create your models here.
class adminmodel(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)

class addproductlist(models.Model):
    # requestid = models.IntegerField(primary_key=True)
    # id=models.BigIntegerField(default=1,primary_key=True)
#    product_name = models.CharField(max_length=100)
    product_name=models.CharField(max_length=100)
    product_description=models.CharField(max_length=100)
    category = models.CharField(max_length=100,null=True)
    #product_image = models.CharField(max_length=100,null=True)
#    product_sku=models.IntegerField(default=1)
    product_sku=models.CharField(max_length=100)
    product_price=models.FloatField()
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True)
    discount_applied = models.BooleanField(default=False)
    discount_price = models.IntegerField(default=0)
    discount_percent = models.IntegerField(default=0)
    #name= models.CharField(max_length=500)
    videofile= models.FileField(upload_to='images/', null=True, verbose_name="")

    reason_for_disapproval=models.CharField(max_length=100,default='None')
    supplier_username=models.CharField(max_length=100)
    is_approved=models.BooleanField(default=False)
    out_of_stock = models.BooleanField(default=False)

class delete_product_list(models.Model):
    product_name=models.CharField(max_length=100)
    product_description=models.CharField(max_length=100)
    product_sku=models.CharField(max_length=100)
    product_price=models.FloatField()
    reason_for_removal=models.TextField(default="")
    supplier_username=models.CharField(max_length=100)
    is_approved=models.BooleanField(default=False)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True)

    reason_for_disapproval=models.CharField(max_length=100,default='None')
