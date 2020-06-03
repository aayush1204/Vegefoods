from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from .models import Product
from shop.models import Supplier
from django.contrib import messages
from .forms import ProductForm
from admindashboard.models import addproductlist

# Create your views here.

def home(request, pk):


    supplier_info = Supplier.objects.get(id=pk)
    return render(request, "dashboard/index.html", {'supplier_info' : supplier_info} )

def supplier_register(request):
    if (request.method == "POST"):
        
        supplier=Supplier()

        supplier.first_name=request.POST['first_name']
        supplier.last_name=request.POST['last_name']
        supplier.email=request.POST['email']
        supplier.address=request.POST['address']
        supplier.pincode=request.POST['pincode']
        supplier.GST_number=request.POST['GST_number']
        supplier.store_name=request.POST['store_name']
        supplier.store_description=request.POST['store_description']
        supplier.store_address=request.POST['store_address']

        supplier.username=request.POST['username']
        supplier.password=request.POST['password']
        supplier.confirm_password=request.POST['confirm_password']

        if(supplier.password==supplier.confirm_password):

            if Supplier.objects.filter(username=supplier.username).exists():
                messages.info(request, "This username is already taken!")
                return render(request, 'dashboard/register.html')


            else:

                supplier.save()
                print("user is hereeeeeeeeeeeeeeee")
                return render(request, 'dashboard/login.html')
        else:
            messages.info(request, "The two passwords don't match! Please enter correct password.")
            return render(request, 'dashboard/register.html' )


    else:

        return render(request, 'dashboard/register.html')


def supplier_login(request):
    if(request.method=="POST"):

        supplier= Supplier()

        supplier.username=request.POST['username']
        supplier.password=request.POST['password']

        try:
                supplier_info = Supplier.objects.get(username=supplier.username)

                if (supplier_info.password ==  supplier.password):

                    return render(request, 'dashboard/index.html', {'supplier_info':supplier_info})
                else:
                    messages.info(request, "Incorrect Password!")
                    return render(request, 'dashboard/login.html')

        except Supplier.DoesNotExist:
                messages.info(request, "User doesnt exist!")
                return render(request, 'dashboard/login.html')




def login(request):
        return render(request, 'dashboard/login.html')



def products(request, pk):

    y=Supplier.objects.get(id=pk)
    prods=[]



    prod = Product.objects.filter(supplier_id = y.id)
    for m in prod:
        prods.append(m)
        print(prods)
    print(prods)

    print(y)
    print(y.id)
    print(prod)
    #print(prod.product_name)
    #print(prod.product_name)
    args = { 'y':y, 'prods' : prods}
    #print(prod.id)


    return render(request, "dashboard/products.html", args)
#    else:
#        print("No products")
#        messages.info(request, "You have not added any products yet!!")
#        return render(request, "dashboard/messagedisplay.html" )



def add(request, pk):

            y=Supplier.objects.get(id=pk)
            print(y)
            print(y.last_name)
            args = { 'y':y }

            return render(request, 'dashboard/add.html', args)

def addnew(request):

    if(request.method=="POST"):
        print(request.POST)

        add_product = Product()
        add_product.product_name=request.POST['product_name']
        add_product.product_description=request.POST['product_description']
        add_product.product_sku=request.POST['product_sku']
        add_product.product_price=request.POST['product_price']
        x=request.POST['supplier']
        y=Supplier.objects.get(username=x)
        add_product.supplier = y


        add_product.save()
        requestobj=addproductlist.objects.create(supplier_username=x,product_sku=request.POST['product_sku'],product_name=request.POST['product_name'],product_price=request.POST['product_price'],product_description=request.POST['product_description'])
        messages.info(request, "Your request has been sent!")
        return render(request, 'dashboard/messagedisplay.html')

def delete(request, pk):

            y=Supplier.objects.get(id=pk)
            print(y)
            print(y.last_name)
            args = { 'y':y }

            return render(request, 'dashboard/delete.html', args)

def delete_existing(request):

    message.info(request, "Request Sent")
    return render(request, 'dashboard/messagedisplay.html')
