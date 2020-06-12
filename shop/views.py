from django.shortcuts import render
from .models import Product ,Cart, Supplier, Signup, User, Address , Order, Supplier, ContactUs, Profile ,Refunds
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import requests
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.utils.datastructures import MultiValueDictKeyError
from django.core.mail import send_mail
import smtplib
from django.conf import settings

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

        DEFAULT_FROM_EMAIL='raoashish1008@gmail.com'

        password='vegefoods1234'

        # send_mail('Order Number: '+str(order.referral_id),'Order placed successfully\nOrder id: {}\nReciepient name: {} {}\nTotal: {}'.format(order.referral_id,fname,lname,total),
        #             settings.DEFAULT_FROM_EMAIL,
        #             recipient_list= [request.user.email],
        #             fail_silently=False,
        #             # html_message=msg
        #             )
        subject='Order Number: '+str(order.referral_id)
        body='Order placed successfully\nOrder id: {}\nReciepient name: {} {}\nTotal: {}'.format(order.referral_id,fname,lname,total)
        msg= f'Subject: {subject}\n\n{body}'
        
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(DEFAULT_FROM_EMAIL,password)
        server.sendmail(DEFAULT_FROM_EMAIL,request.user.email,msg)
        server.quit()
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
        # orders = Order.objects.filter(user=request.user).filter(referral_id=x)
        # dic={}
        # for i in orders:
        #     for j in i.items.all():
        #         print(j.product.id)
        #         b=str(j.product.id)
        #         try:
        #             a = request.POST[b]
        #         except MultiValueDictKeyError:
        #             a = 'No'
        #         # a=request.POST.get(b, False)
        #         dic[b]=a
        # print(dic)
        # o = Order.objects.get(referral_id=x)
        # r = Refunds.objects.create(order=o, refund_amount=0)
        # for key,val in dic.items():

        #     money=0
        #     o = Order.objects.get(referral_id=x)
        #     for j in o.items.all():
        #         # print(key)
        #         # print(int(j.product.id)==int(key))
        #         if int(j.product.id)==int(key):
        #             # print("hello")
        #             # print(val)
        #             if val=="Yes":
        #                 # messages.info(request, 'Alre!')
        #                 # print(o)
        #                 r.items.add(j)
        #                 r.save()
        #                 # print(money)
        #                 money=money+int(j.product.product_price)*int(j.quantity)
        #                 # print("yes")
        #                 # print(int(j.product.product_price)*int(j.quantity))
        #                 # print(money)
        #                 # q=Order.objects.filter(user=request.user).filter(referral_id=x).filter(items=cf)#.update(refunded=True)
        #                 # o.save()
        #     for i in o.items.all():
        #         r.supplier.add(i.product.supplier)
        #         r.save()
        #     Refunds.objects.filter(order=o).update(refund_amount=money)
        #     if money:
        #         messages.info(request, 'Alre!')

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


        money=0
        for key,val in dic.items():


            # o = Order.objects.get(referral_id=x)
            for j in o.items.all():
                # print(key)
                # print(int(j.product.id)==int(key))
                if int(j.product.id)==int(key):
                    # print("hello")
                    # print(val)
                    if val=="Yes":

                        a = Refunds.objects.filter(order=o).filter(supplier=j.product.supplier)
                        print(a)
                        if a:
                            print("yes")
                            x = int(j.product.product_price)*int(j.quantity)
                            y=int(a[0].refund_amount)
                            a.update(refund_amount=x+y)
                            a[0].items.add(j)
                            a[0].save()
                        else:


                            money=int(j.product.product_price)*int(j.quantity)
                            r = Refunds.objects.create(order=o, refund_amount=money , supplier=j.product.supplier)
                            print("no")
                            # messages.info(request, 'Alre!')
                            # print(o)
                            r.items.add(j)
                            # r.supplier.add(j.product.supplier)
                            r.save()


            print(Refunds.objects.all())

            if money:
                messages.info(request, 'Alre!')
                Order.objects.filter(user=request.user).filter(referral_id=x).update(is_refunded=True)


        return render(request, 'refund.html',{'orders':orders})



    orders = Order.objects.filter(user=request.user).filter(referral_id=x)
    return render(request, 'refund.html', {'orders':orders})

def track(request, x):
    orders = Order.objects.filter(referral_id=x)
    approved='active'
    shipped=''
    delivered=''
    text="Placed"

    if (orders[0].is_approved == True):
        approved='visited'
        shipped='active'
        delivered=''
        text="Order Approved"
    if (orders[0].is_shipped):
        approved='visited'
        shipped='visited'
        delivered='active'
        text="Shipped"
    if (orders[0].is_completed):
        approved='visited'
        shipped='visited'
        delivered='visited next'
        text="Delivered"


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

def myrefunds(request):
    # x = Order.objects.filter(user=request.user)
    z = User.objects.get(username=request.user.username)
    w = Refunds.objects.filter(order__user = z)
    print(w)
    # ls=[]
    # for i in x:
    #     try:
    #         if Refunds.objects.get(order=i):
    #             print(i.referral_id)
    #             ls.append(Refunds.objects.get(order=i))
    #     except Refunds.DoesNotExist:
    #         continue
    # print(ls)

    return render(request, 'myrefunds.html',{'rdata':w})
