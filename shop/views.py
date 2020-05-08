from django.shortcuts import render
from .models import Product
# Create your views here.

def home(request):

    product_data = Product.objects.all()
    for i in product_data:

        print(i.product_image)
    return render(request,'index.html',{'pdata':product_data})

def product_single(request, name):

    pdata = Product.objects.get(product_name=name)
    
    return render(request, 'product-single.html',{'pdata':pdata})
