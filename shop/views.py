from django.shortcuts import render
from .models import Product ,Cart
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

def home(request):

    product_data = Product.objects.all()
    for i in product_data:

        print(i.product_image)
    return render(request,'index.html',{'pdata':product_data})

def product_single(request, name):

    pdata = Product.objects.get(product_name=name)
    print(pdata.supplier_name.supplier_name)
    return render(request, 'product-single.html',{'pdata':pdata})

def add_cart(request, name):
    if request.method == "POST":
        
        quantity = request.POST['quantity']
        pddata = Product.objects.get(product_name=name)
        price = int(pddata.product_price)
        tp=int(quantity)*price
        
        
        try:
            p = Cart.objects.get(product=pddata)
            pdata = Product.objects.get(product_name=name)
            print(pdata.supplier_name.supplier_name)
            messages.info(request, 'Already added in cart!')
            return render(request, 'product-single.html',{'pdata':pdata})

        except Cart.DoesNotExist:

            cdata = Cart.objects.create(product=pddata, quantity=quantity,
                                    product_image=pddata.product_image)
            cdata.save()
        
            product_data = Product.objects.all()
            cart_data = Cart.objects.all()
            total_bill = int(0)
            for j in cart_data:
                total_bill += j.quantity*int(j.product.product_price) 
        # return render(request, 'index.html',{'pdata':product_data})
            return render(request, 'cart.html',{'cdata':cart_data,'stbill':total_bill})
        
           
def cart_view(request):

    cart_data = Cart.objects.all()
    total_bill = int(0)
    for j in cart_data:
        total_bill += j.quantity*int(j.product.product_price) 

    return render(request,'cart.html',{'cdata':cart_data,'stbill':total_bill})

def shop_view(request):

    product_list = Product.objects.all()
    # for i in product_data:

        # print(i.product_image)

    # company_list= Companies.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(product_list, 2)

    try:
        product_data = paginator.page(page)
    except PageNotAnInteger:
        product_data = paginator.page(1)
    except EmptyPage:
        product_data = paginator.page(paginator.num_pages)

    # return render(request, 'job-listings.html', {'company_data': company_data}) 
    all1='active'
    fruit=""
    dairy=""
    return render(request,'shop.html',{'pdata':product_data,'all':all1,'fruit':fruit,'dairy':dairy})    

def filter(request, name):
    product_list = Product.objects.filter(category__icontains=name)
    # for i in product_data:

        # print(i.product_image)

    # company_list= Companies.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(product_list, 1)

    try:
        product_data = paginator.page(page)
    except PageNotAnInteger:
        product_data = paginator.page(1)
    except EmptyPage:
        product_data = paginator.page(paginator.num_pages)

    # return render(request, 'job-listings.html', {'company_data': company_data}) 
    all1=""
     
    fruit=""
    dairy=""
    if name=="Fruits":
        fruit='active'
    elif name=='Dairy':
        dairy='active'    
    return render(request,'shop.html',{'pdata':product_data,'all':all1,'fruit':fruit,'dairy':dairy})

def checkout_view(request):
    
    subtotal = request.GET['totalbill'] 
    cdata = Cart.objects.all() 
    quantities=[]
    prices=[]
    str1=""
    for i in cdata:
        str1=str(i.product.product_name) + 'quantity'
        quantities.append(request.GET[str1])
        str1=str(i.product.product_name) + 'price'
        prices.append(request.GET[str1][3:])
    count=0
    for i in cdata:
        Cart.objects.filter(product=i.product).update(quantity=quantities[count])   
        count=count+1
    print(prices)    
    return render(request, 'checkout.html',{"stbill":subtotal}) 

