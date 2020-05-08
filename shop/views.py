from django.shortcuts import render
from .models import Product ,Cart
# Create your views here.

def home(request):

    product_data = Product.objects.all()
    for i in product_data:

        print(i.product_image)
    return render(request,'index.html',{'pdata':product_data})

def product_single(request, name):

    pdata = Product.objects.get(product_name=name)
    
    return render(request, 'product-single.html',{'pdata':pdata})

def add_cart(request, name):
    if request.method == "POST":
        
        quantity = request.POST['quantity']
        pddata = Product.objects.get(product_name=name)
        price = int(pddata.product_price)
        tp=int(quantity)*price

        cdata = Cart.objects.create(product_name=name, total_price=tp, quantity=quantity,
                                    product_price=price, product_image=pddata.product_image)
        cdata.save()
        
        product_data = Product.objects.all()
        cart_data = Cart.objects.all()
        total_bill = int(0)
        for j in cart_data:
            total_bill += j.total_price 
        # return render(request, 'index.html',{'pdata':product_data})
        return render(request, 'cart.html',{'cdata':cart_data,'tbill':total_bill})

def cart_view(request):

    cart_data = Cart.objects.all()
    total_bill = int(0)
    for j in cart_data:
        total_bill += j.total_price 

    return render(request,'cart.html',{'cdata':cart_data,'tbill':total_bill})

