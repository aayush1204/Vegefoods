from django.shortcuts import render
from .models import Product ,Cart, Supplier, Signup, User, Address , Order, Supplier, ContactUs, Profile ,Refunds
from django.contrib import messages
from shop.models import OrderSupplier
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import requests
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.utils.datastructures import MultiValueDictKeyError
from django.db.models import Q

from django.core.mail import send_mail
import smtplib
# from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

from django.template.loader import get_template
from django.template import Context
import pdfkit

import os
from django.conf import settings

import threading

from random import shuffle
# Create your views here.

class EmailThread(threading.Thread):
    def __init__(self, DEFAULT_FROM_EMAIL,msg, password, user):
        threading.Thread.__init__(self)
        self.msg = msg
        self.DEFAULT_FROM_EMAIL = DEFAULT_FROM_EMAIL
        self.password = password
        self.user = user
        
    
    def run(self):
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        print(self.DEFAULT_FROM_EMAIL)
        print(self.password)
        
        server.login(self.DEFAULT_FROM_EMAIL,self.password)
        server.sendmail(self.DEFAULT_FROM_EMAIL,self.user.email,self.msg.as_string())
        server.quit() 
        # sendmail(DEFAULT_FROM_EMAIL,request.user.email,msg.as_string())    


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
        if pddata.discount_applied ==False:
            price = int(pddata.product_price)
        else:
            price = int(pddata.discount_price)
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
                                    product_image=pddata.product_image,user=request.user,product_price=tp)
            cdata.save()

            product_data = Product.objects.all()
            cart_data = Cart.objects.filter(is_ordered=False).filter(user=request.user)
            total_bill = int(0)
            for j in cart_data:
                if j.product.discount_applied==False:
                    total_bill += j.quantity*int(j.product.product_price)
                else:
                    total_bill += j.quantity*int(j.product.discount_price)
        # return render(request, 'index.html',{'pdata':product_data})
            z = User.objects.filter(username=request.user.username)

            profile = Profile.objects.get(user=z[0])
            return render(request, 'cart.html',{'cdata':cart_data,'stbill':total_bill, 'profiledata':profile})

def delete_cart(request,p):
    Cart.objects.get(id=p).delete()
    cart_data = Cart.objects.filter(is_ordered=False).filter(user=request.user)

    total_bill = int(0)
    for j in cart_data:
        if j.product.discount_applied == False:
            total_bill += j.quantity*int(j.product.product_price)
        else:
            total_bill += j.quantity*int(j.product.discount_price)


    return render(request,'cart.html',{'cdata':cart_data,'stbill':total_bill})
def cart_view(request):

    cart_data = Cart.objects.filter(is_ordered=False).filter(user=request.user)

    total_bill = int(0)
    for j in cart_data:
        if j.product.discount_applied == False:
            total_bill += j.quantity*int(j.product.product_price)
        else:
            total_bill += j.quantity*int(j.product.discount_price)

    z = User.objects.filter(username=request.user.username)

    profile = Profile.objects.get(user=z[0])

    return render(request,'cart.html',{'cdata':cart_data,'stbill':total_bill, 'profiledata':profile})

def shop_view(request):
    print("shopview")
    
    product_list = Product.objects.filter(out_of_stock=False).order_by('rank','supplier__package','product_name')
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

def searchMatch(query, item):
    
    if query in item.description.lower() or query in item.category.lower() or query in item.product_name.lower():
        return True 
    elif query in item.description or query in item.category or query in item.product_name:
        return True     
    return False

def search(request):
    if request.method== 'GET':
        query = request.GET['search_query']

        product_temp = Product.objects.filter(out_of_stock=False)
        # product_list = [item for item in product_temp if searchMatch(query, item)]
        product_list = Product.objects.filter( Q(product_name__icontains=query)| Q(description__icontains=query)
                                            | Q(category__icontains=query) ).order_by('rank','supplier__package','product_name')
        print(product_list)
        print('yes')
        print(query)
        
        if len(product_list) == 0:
            messages.info(request, 'Alre!')
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
    print('filter')
    product_list = Product.objects.filter(category__icontains=name).filter(out_of_stock=False).order_by('rank','supplier__package','product_name')
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

    address_data = Address.objects.filter(user=request.user)

    z = User.objects.filter(username=request.user.username)

    profile = Profile.objects.get(user=z[0])

    discount = 0
    if profile.orders_placed<5:
        discount = profile.society.corporate_discount
        discount = int(discount*int(subtotal)/100)
    total = int(subtotal) - int(discount)
    return render(request, 'checkout.html',{"stbill":subtotal, 'adata':address_data, 'profiledata':profile,
                                            "total": total, "discount":discount, })

def order_place(request):

    if request.method=="POST":
        fname = request.POST['firstname']
        lname = request.POST['lastname']

        state = request.POST['state']
        address =  request.POST['streetaddress']
        apartmentno =  request.POST['apartmentno']
        city =  request.POST['towncity']
        zipcode = request.POST['postcodezip']
        phone=request.POST['phone']
        # Address.objects.create(state=state,address=address,apartmentno=apartmentno,city=city,zipcode=zipcode,
                                # category="1", user = request.user)
        print(fname)
        print(state)
        total = request.POST['totalbill']
        total=int(total[3:])

        order = Order.objects.create(user=request.user ,state=state,address=address,apartmentno=apartmentno,city=city,zipcode=zipcode,
                                     total_amount = total)

        order.save()
        x = User.objects.get(username=request.user.username)
        us = Profile.objects.filter(user=x)
        print(us)
        print(us[0].orders_placed)
        a = int(us[0].orders_placed)
        a=a+1
        Profile.objects.filter(user=x).update(orders_placed=a)

        DEFAULT_FROM_EMAIL='raoashish1008@gmail.com'

        password='vegefoods1234'

        cdata =  Cart.objects.filter(is_ordered=False)
        for i in cdata:

            order.supplier.add(i.product.supplier)
            order.items.add(i)

        order.save()
        refid = int(order.referral_id)
        for j in order.supplier.all():
            ordersupplier = OrderSupplier.objects.create(referral_id=refid, user=request.user,
                                                            state=state,address=address, apartmentno=apartmentno, city=city,zipcode=zipcode,supplier=j)
            amount=0
            for i in order.items.all():
                if i.product.supplier == j:
                    ordersupplier.items.add(i)
                    ordersupplier.save()
                    if i.product.discount_applied == True:
                        amount = amount + int(i.quantity)*int(i.product.discount_price)
                    else:
                        amount = amount + int(i.quantity)*int(i.product.product_price)

            ordersupplier.total_amount = amount
            ordersupplier.save()




        Cart.objects.filter(is_ordered=False).update(is_ordered=True)
        address=apartmentno+', '+address+', '+city+' - '+zipcode

        #### Customer Invoice ####
        template = get_template("admin/ordertemplate.html")
        # context = Context({"orgdata": order})
        html = template.render({'orgdata':order,'address':address})

        path_wkhtmltopdf = os.path.join(os.getcwd(),r'wkhtmltox\bin\wkhtmltopdf.exe')
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

        pdfkit.from_string(html, 'out.pdf',configuration=config)
            # response = HttpResponse(pdf.read(), content_type='application/pdf')  # Generates the response as pdf response.
        # response['Content-Disposition'] = 'attachment; filename=output.pdf'

        msg = MIMEMultipart()
        msg['Subject'] = 'Order Number: '+str(order.referral_id)
        body = MIMEText('Hello {}! Your order details have been attached with this mail. We request you to save this file and show it during the time of delivery. '.format(x.first_name))
        msg.attach(body)

        fp = open(r'out.pdf', 'rb')

        # img = MIMEImage(fp.read())
        # msg.attach(fp.read())

        attach = MIMEApplication(fp.read(),_subtype="pdf")
        fp.close()
        attach.add_header('Content-Disposition','attachment',filename=str(r'{}.pdf'.format(order.referral_id)))
        msg.attach(attach)

        # server = smtplib.SMTP('smtp.gmail.com:587')
        # server.starttls()
        # server.login(DEFAULT_FROM_EMAIL,password)
        # server.sendmail(DEFAULT_FROM_EMAIL,request.user.email,msg.as_string())
        # EmailThread(DEFAULT_FROM_EMAIL,msg,password).start()
        user = request.user
        p = EmailThread(DEFAULT_FROM_EMAIL,msg,password, user)
        p.start()
        # server.quit()
        os.remove("out.pdf")

        #### Supplier Report ####

        # phone=request.user.phone
        template = get_template("admin/suppliertemplate.html")
        for i in order.supplier.all():
            html = template.render({'orgdata':order,'address':address,'phone':phone,'suppdata':i})
            path_wkhtmltopdf = os.path.join(os.getcwd(),r'wkhtmltox\bin\wkhtmltopdf.exe')
            config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

            pdfkit.from_string(html, 'out.pdf',configuration=config)
            msg = MIMEMultipart()
            msg['Subject'] = 'Order Number: '+str(order.referral_id)
            body = MIMEText('Hello {}! Here is the report for order number {}'.format(i.supplier_details.first_name,order.referral_id))
            msg.attach(body)

            fp = open(r'out.pdf', 'rb')

            # img = MIMEImage(fp.read())
            # msg.attach(fp.read())

            attach = MIMEApplication(fp.read(),_subtype="pdf")
            fp.close()
            attach.add_header('Content-Disposition','attachment',filename=str(r'{}.pdf'.format(order.referral_id)))
            msg.attach(attach)

            # server = smtplib.SMTP('smtp.gmail.com:587')
            # server.starttls()
            # server.login(DEFAULT_FROM_EMAIL,password)
            # print(i.supplier_details.email)
            # server.sendmail(DEFAULT_FROM_EMAIL,i.supplier_details.email,msg.as_string())
            # server.quit()
            user = i.supplier_details
            p = EmailThread(DEFAULT_FROM_EMAIL,msg,password, user)
            p.start()
            os.remove("out.pdf")



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
                            if j.product.discount_applied == False:
                                x = int(j.product.product_price)*int(j.quantity)
                            else:
                                x = int(j.product.discount_price)*int(j.quantity)
                            y=int(a[0].refund_amount)
                            a.update(refund_amount=x+y)
                            a[0].items.add(j)
                            a[0].save()
                        else:

                            if j.product.discount_applied == False:
                                money=int(j.product.product_price)*int(j.quantity)
                            else:
                                money=int(j.product.discount_price)*int(j.quantity)

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
    orders = Order.objects.filter(items__id=x)
    # approved='active'
    # shipped=''
    # delivered=''
    # text="Placed"

    # if (orders[0].is_approved == True):
    #     approved='visited'
    #     shipped='active'
    #     delivered=''
    #     text="Order Approved"
    # if (orders[0].is_shipped):
    #     approved='visited'
    #     shipped='visited'
    #     delivered='active'
    #     text="Shipped"
    # if (orders[0].is_completed):
    #     approved='visited'
    #     shipped='visited'
    #     delivered='visited next'
    #     text="Delivered"

    orderitem = Cart.objects.filter(id=x)
    approved='active'
    shipped=''
    delivered=''
    text="Placed"

    if (orderitem[0].is_approved == True):
        approved='visited'
        shipped='active'
        delivered=''
        text="Order Approved"
    if (orderitem[0].is_shipped):
        approved='visited'
        shipped='visited'
        delivered='active'
        text="Shipped"
    if (orderitem[0].is_completed):
        approved='visited'
        shipped='visited'
        delivered='visited next'
        text="Delivered"
    itemprice = orderitem[0].product.product_price*orderitem[0].quantity
    no_of_items = orders[0].items.all().count()

    return render(request, 'ordertrack.html', {'orders':orders,'orderitem':orderitem[0],'approved':approved,'shipped':shipped,
                                                'itemprice':itemprice,'delivered':delivered,'text':text,'no':no_of_items })

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

def myaddress(request):

    if request.method=='POST':
        # first_name=request.POST['first_name']
        # last_name=request.POST['last_name']

        category = request.POST['optradio']
        print(category)
        # society = request.POST['society']
        state = request.POST['state']
        address =  request.POST['streetaddress']
        apartmentno =  request.POST['apartmentno']
        city =  request.POST['towncity']
        zipcode = request.POST['postcodezip']

        try:
            address_data = Address.objects.filter(user=request.user).get(category=category)
            address_data = Address.objects.filter(user=request.user).filter(category=category).update(state=state,address=address,
                                                                        apartmentno=apartmentno,city=city,zipcode=zipcode)

        except Address.DoesNotExist:
            Address.objects.create(state=state,address=address,apartmentno=apartmentno,city=city,zipcode=zipcode,
                                category="2", user = request.user)

            print("no")
        a=2
        address = Address.objects.filter(user=request.user)
        messages.info(request, "Updated successfully")
        return render(request, 'myaddress.html', {'adata':address, 'a':a})
    else:
        address_data = Address.objects.filter(user=request.user)
        print(address_data.count())
        a=0
        if address_data.count() == 1:
            a = 1
        messages.info(request, "Updated successfully")
        return render(request, 'myaddress.html', {'adata':address_data, 'a':a})
