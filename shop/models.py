from django.db import models
from accounts.models import Signup
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.
# class Product(models.Model):
#     product_name = models.CharField(max_length=100)
#     product_price = models.IntegerField(default=0)
#     out_of_stock = models.BooleanField(default=False)
#     category = models.CharField(max_length=100)
#     product_image = models.CharField(max_length=100)

# class Cart(models.Model):
#     product_name = models.CharField(max_length=100)
#     total_price = models.IntegerField(default=0)
#     quantity = models.IntegerField(default=0)
#     product_image = models.CharField(max_length=100)
#     product_price = models.IntegerField(default=0)


# New MOdels    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    PR = (
        ('S', 'Supplier'),
        ('C', 'Customer'),
        ('A','Admin'),
    )
    pr= models.CharField(max_length=1,choices=PR)


class Supplier(models.Model):
    
    supplier_details = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    phone = models.CharField(max_length=10) 
    
    address = models.TextField(default="")
    number = models.CharField(max_length=15)
    #address = models.TextField()
    pincode=models.PositiveIntegerField(default=0)
    GST_number=models.PositiveIntegerField(default=0)
    Bank_Account_Details=models.TextField(default="")
    store_name = models.CharField(max_length=50)
    store_description = models.CharField(max_length=200)
    store_address=models.TextField(default="")
#   product = ForeignKey
    is_approved = models.BooleanField(default=False)
    #signature-will be an image

    def __str__(self):
        return self.store_name

class Product(models.Model):
    product_name = models.CharField(max_length=100)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True)
    description = models.CharField(max_length=150)
    product_price = models.IntegerField(default=0)
    out_of_stock = models.BooleanField(default=False)
    category = models.CharField(max_length=100)
    product_image = models.CharField(max_length=100)
    product_sku=models.IntegerField(default=1)
    

    def __str__(self):
        return self.product_name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    # total_price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    product_image = models.CharField(max_length=100)
    is_ordered = models.BooleanField(default=False)
    # product_price = models.IntegerField(default=0)

    def __str__(self):
        return self.product.product_name

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    state = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    apartmentno = models.CharField(max_length=10)
    city = models.CharField(max_length=20)
    zipcode = models.CharField(max_length=6)
    ch = (
        ('1', 'Category1'),
        ('2', 'Category2'),
    )
    category= models.CharField(max_length=1,choices=ch)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    referral_id = models.AutoField(primary_key=True)
    supplier = models.ManyToManyField(Supplier)
    order_date = models.DateTimeField(auto_now=True)
    state = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    apartmentno = models.CharField(max_length=10)
    city = models.CharField(max_length=20)
    zipcode = models.CharField(max_length=6) 
    is_completed = models.BooleanField(default=False)
    total_amount = models.IntegerField(default=0)
    items = models.ManyToManyField(Cart)
    is_refunded = models.BooleanField(default=False)   
    
    def __str__(self):
        return self.referral_id

class ContactUs(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=254)
    subject = models.CharField(max_length=20)
    message = models.CharField(max_length=200)
    is_addressed = models.BooleanField(default=False)

    def __str__(self):
        return self.subject
