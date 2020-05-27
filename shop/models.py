from django.db import models

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

class Supplier(models.Model):
    supplier_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10) 

class Product(models.Model):
    product_name = models.CharField(max_length=100)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True)
    description = models.CharField(max_length=150)
    product_price = models.IntegerField(default=0)
    out_of_stock = models.BooleanField(default=False)
    category = models.CharField(max_length=100)
    product_image = models.CharField(max_length=100)

class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    # total_price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    product_image = models.CharField(max_length=100)
    is_ordered = models.BooleanField(default=False)
    # product_price = models.IntegerField(default=0)

class Address(models.Model):
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