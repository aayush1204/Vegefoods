from django.shortcuts import render
from .models import Product ,Cart, Supplier, Signup, User, Address , Order, Supplier
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import requests
# Create your views here.

def home(request):

    product_data = Product.objects.filter(out_of_stock=False)
    for i in product_data:

        print(i.product_image)
    return render(request,'index.html',{'pdata':product_data})

def product_single(request, q):

    pdata = Product.objects.get(id=q)
    print(pdata.supplier.supplier_name)
    return render(request, 'product-single.html',{'pdata':pdata})

def add_cart(request, q):
    if request.method == "POST":
        
        quantity = request.POST['quantity']
        pddata = Product.objects.get(id=q)
        price = int(pddata.product_price)
        tp=int(quantity)*price
        print(request.user)
        
        userdata = User.objects.all()
        # for i in userdata:
            # if request.user == i:
        print(userdata)
            
        try:
            p = Cart.objects.filter(is_ordered=False).filter(user=request.user).get(product=pddata)
            pdata = Product.objects.get(id=q)
            print(pdata.supplier.supplier_name)
            messages.info(request, 'Already added in cart!')
            return render(request, 'product-single.html',{'pdata':pdata})

        except Cart.DoesNotExist:

            cdata = Cart.objects.create(product=pddata, quantity=quantity,
                                    product_image=pddata.product_image,user=request.user)
            cdata.save()
        
            product_data = Product.objects.all()
            cart_data = Cart.objects.filter(is_ordered=False).filter(user=request.user)
            total_bill = int(0)
            for j in cart_data:
                total_bill += j.quantity*int(j.product.product_price) 
        # return render(request, 'index.html',{'pdata':product_data})
            return render(request, 'cart.html',{'cdata':cart_data,'stbill':total_bill})
        
def delete_cart(request,p):
    Cart.objects.get(id=p).delete()
    cart_data = Cart.objects.filter(is_ordered=False).filter(user=request.user)

    total_bill = int(0)
    for j in cart_data:

        total_bill += j.quantity*int(j.product.product_price) 

    return render(request,'cart.html',{'cdata':cart_data,'stbill':total_bill})           
def cart_view(request):

    cart_data = Cart.objects.filter(is_ordered=False).filter(user=request.user)

    total_bill = int(0)
    for j in cart_data:

        total_bill += j.quantity*int(j.product.product_price) 

    return render(request,'cart.html',{'cdata':cart_data,'stbill':total_bill})

def shop_view(request):

    product_list = Product.objects.filter(out_of_stock=False)
    # for i in product_data:

        # print(i.product_image)

    # company_list= Companies.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(product_list, 8)

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
    vegetables=""
    juices=""
    return render(request,'shop.html',{'pdata':product_data,'all':all1,'fruit':fruit,
                                        'dairy':dairy,'vegetable':vegetables,'juice':juices})    

def filter(request, name):
    product_list = Product.objects.filter(category__icontains=name).filter(out_of_stock=False)
    # for i in product_data:

        # print(i.product_image)

    # company_list= Companies.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(product_list, 8)

    try:
        product_data = paginator.page(page)
    except PageNotAnInteger:
        product_data = paginator.page(1)
    except EmptyPage:
        product_data = paginator.page(paginator.num_pages)

    # return render(request, 'job-listings.html', {'company_data': company_data}) 
    all1=""
    vegetables=""
    juices="" 
    fruit=""
    dairy=""
    if name=="Fruits":
        fruit='active'
    elif name=='Dairy':
        dairy='active' 
    elif name=='Vegetables':
        vegetables='active' 
    elif name=='Juices':
        juices='active'            
    return render(request,'shop.html',{'pdata':product_data,'all':all1,'fruit':fruit,'dairy':dairy,
                                            'vegetable':vegetables,'juice':juices})

def checkout_view(request):
    
    subtotal = request.GET['totalbill'] 
    ab = subtotal[3:]
    subtotal=ab
    cdata = Cart.objects.filter(is_ordered=False).filter(user=request.user) 
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

    address_data = Address.objects.filter(user=request.user).last()
    return render(request, 'checkout.html',{"stbill":subtotal, 'adata':address_data}) 

def order_place(request):

    if request.method=="POST":
        fname = request.POST['firstname']
        lname = request.POST['lastname']

        state = request.POST['state']
        address =  request.POST['streetaddress']
        apartmentno =  request.POST['apartmentno']
        city =  request.POST['towncity']
        zipcode = request.POST['postcodezip']

        Address.objects.create(state=state,address=address,apartmentno=apartmentno,city=city,zipcode=zipcode,
                                category="1", user = request.user)
        print(fname)
        print(state)
        total = request.POST['totalbill'] 
        total=int(total[3:])

        order = Order.objects.create(user=request.user ,state=state,address=address,apartmentno=apartmentno,city=city,zipcode=zipcode,
                                     total_amount = total)
        order.save()
        cdata =  Cart.objects.filter(is_ordered=False)
        for i in cdata:

            order.supplier.add(i.product.supplier)
            order.items.add(i) 
            
        order.save()
        Cart.objects.filter(is_ordered=False).update(is_ordered=True)                                
    product_data=Product.objects.filter(out_of_stock=False)
    messages.info(request, 'Alre!')
    return render(request,'index.html',)

def myorders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'myorders.html', {'orders':orders})

def contact(request):
    return render(request, 'contact.html')

