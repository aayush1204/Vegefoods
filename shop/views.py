from django.shortcuts import render
from .models import Product ,Cart, Supplier, Signup, User, Address , Order, Supplier, ContactUs, Profile, Refunds
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import requests
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.utils.datastructures import MultiValueDictKeyError

# Create your views here.

def home(request):

    product_data = Product.objects.filter(out_of_stock=False)
    for i in product_data:

        print(i.product_image)
    return render(request,'index.html',{'pdata':product_data})

def product_single(request, q):

    pdata = Product.objects.get(id=q)
    # print(pdata.supplier.supplier_name)
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
            # print(pdata.supplier.supplier_name)
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

def refund(request, x):

    if request.method=="POST":
        orders = Order.objects.filter(user=request.user).filter(referral_id=x)
        dic={}
        for i in orders:
            for j in i.items.all():
                print(j.product.id)
                b=str(j.product.id)
                try:
                    a = request.POST[b]
                except MultiValueDictKeyError:
                    a = 'No'
                # a=request.POST.get(b, False)
                dic[b]=a
        print(dic)
        o = Order.objects.get(referral_id=x)
        r = Refunds.objects.create(order=o, refund_amount=0)
        money=0
        for key,val in dic.items():
                 
            o = Order.objects.get(referral_id=x)
            for j in o.items.all():
                print(key)
                print(int(j.product.id)==int(key))
                if int(j.product.id)==int(key):
                    # print("hello")
                    # print(val)
                    if val=="Yes":
                        
                        # print(o)
                        r.items.add(j)
                        r.save()
                        print(money)
                        money=money+int(j.product.product_price)*int(j.quantity)
                        # print("yes")
                        print(int(j.product.product_price)*int(j.quantity))
                        print(money)
                        # q=Order.objects.filter(user=request.user).filter(referral_id=x).filter(items=cf)#.update(refunded=True)
                        # o.save()  
        print(money)  
        if money:
            messages.info(request, 'Alre!')          
        Refunds.objects.filter(order=o).update(refund_amount=money)


        return render(request, 'refund.html',{'orders':orders})        



    orders = Order.objects.filter(user=request.user).filter(referral_id=x)
    return render(request, 'refund.html', {'orders':orders})

def track(request, x):
    orders = Order.objects.filter(referral_id=x)
    approved='active'
    shipped=''
    delivered=''   
    text="Placed" 
    if orders[0].is_completed==True:
        approved='visited'
        shipped='visited'
        delivered='visited next'
        text="Delivered"        
    if orders[0].is_shipped==True:
        approved='visited'
        shipped='visited'
        delivered='active'
        text="Shipped"
    if orders[0].is_approved==True:
        approved='visited'
        shipped='active'
        delivered=''
        text="Order Approved"        

    return render(request, 'ordertrack.html', {'orders':orders,'approved':approved,'shipped':shipped,
                                                               'delivered':delivered,'text':text })

def contact(request):

    if request.method=="POST":
        name= request.POST['name']
        email = request.POST['email']
        subject=request.POST['subject']
        message = request.POST['message']
        complaint = ContactUs.objects.create(name=name,email=email,subject=subject,message=message)
        complaint.save()
        messages.info(request, 'Message Sent! We will contact you shortly')
        return render(request, 'contact.html')

    return render(request, 'contact.html')



def sellwithus(request):
    if (request.method == "POST"):

        supplier=Supplier()
        
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        supplier.address=request.POST['address']
        supplier.pincode=request.POST['pincode']
        supplier.GST_number=request.POST['GST_number']
        supplier.store_name=request.POST['store_name']
        supplier.store_description=request.POST['store_description']
        supplier.store_address=request.POST['store_address']

        username=request.POST['username']
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']

        if(password==confirm_password):

            if User.objects.filter(username=username).exists():
                messages.info(request, "This username is already taken!")
                return render(request, 'supplier_register.html')


            else:
                user = User.objects.create_user(first_name=first_name, last_name=last_name,email=email,username=username,password=password)

                user.save()
                Profile.objects.create(user=user,pr='S')
                supplier.supplier_details=user
                
                supplier.save()
                print("user is hereeeeeeeeeeeeeeee")
                return render(request, 'supplier_login.html')
        else:
            messages.info(request, "The two passwords don't match! Please enter correct password.")
            return render(request, 'supplier_register.html' )


    else:

        return render(request, 'supplier_register.html')


def supplier_login(request):
    if(request.method=="POST"):

        supplier= Supplier()

        username=request.POST['username']
        password=request.POST['password']

        try:
                supplier_in = User.objects.get(username=username)
                print(password)
                print(supplier_in.password)

                user =  auth.authenticate(username=username,password=password)
                print(user.profile.pr)

                if (user.profile.pr=='S'):
                    auth.login(request, user)
                    return redirect('/')
                else:
                    messages.info(request, "Incorrect Credentials. Please enter the correct ones!")
                    return render(request, 'supplier_login.html')

                # if (supplier_in.password ==  password):
                #     supplier_info = Supplier.objects.filter(supplier_details=supplier_in)
                #     return render(request, 'index.html', {'supplier_info':supplier_info})
                # else:
                #     messages.info(request, "Incorrect Password!")
                #     return render(request, 'supplier_login.html')

        except User.DoesNotExist:
                messages.info(request, "User doesnt exist!")
                return render(request, 'supplier_login.html')

    return render(request, 'supplier_login.html')            

