from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from shop.models import Product, Order
from shop.models import Supplier, Profile ,Refunds
from django.contrib import messages
#from .forms import ProductForm
from admindashboard.models import addproductlist,delete_product_list

# Create your views here.

def home(request):



    return render(request, "dashboard/supplier_index")


def supplier_index(request):


    supplier_info = Supplier.objects.get(supplier_details=request.user)
    #print(user.supplier.store_name)
    return render(request, "dashboard/supplier_index.html", {'supplier_info' : supplier_info} )


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
                elif user.profile.pr=='A':
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
        except:
                messages.info(request, "Incorrect Credentials!")
                return render(request, 'supplier_login.html')        


    return render(request, 'supplier_login.html')



def login(request):
        return render(request, 'dashboard/login.html')



def products(request):

#    y=Supplier.objects.get(id=pk)
    prods=[]
    colors=["success","warning","info","primary"]
    x = User.objects.get(username=request.user.username)
    y=Supplier.objects.get(supplier_details=x)
    print(y.store_description)
    prod = Product.objects.filter(supplier = y)


    #prod = Product.objects.filter()
    if prod.exists():
            for m in prod:
                prods.append(m)
                print(prods)
                print(prods)

            args = { 'prods' : prods, 'y':y, 'colors':colors}

            return render(request, "dashboard/products.html", args)
    else:
#        print("No products")
        messages.info(request, "You have not added any products yet!! Please click on the 'Addition on New Products' tab to add a prodcut")
        return render(request, "dashboard/products.html" )



def add(request):


            p = Supplier.objects.get(supplier_details=request.user)

            return render(request, 'dashboard/add.html',{ 'p':p })

def addnew(request):

    if(request.method=="POST"):
        print(request.POST)

        #add_product = Product()
        #add_product.product_name=request.POST['product_name']
        #add_product.product_description=request.POST['product_description']
        #add_product.product_sku=request.POST['product_sku']
        #add_product.product_price=request.POST['product_price']
        #x=request.POST['supplier']
        #y=Supplier.objects.get(username=x)
        #add_product.supplier = y


        #add_product.save()
        requestobj=addproductlist.objects.create(supplier_username=request.user.username,product_sku=request.POST['product_sku'],product_name=request.POST['product_name'],product_price=request.POST['product_price'],product_description=request.POST['product_description'])
        messages.info(request, "Your request has been sent!")
        return render(request, 'dashboard/messagedisplay.html')

def delete(request):

        #    y=Supplier.objects.get(id=pk)
        #    print(y)
        #    print(y.last_name)
        #    args = { 'y':y }

            return render(request, 'dashboard/delete.html')#, args)

def delete_existing(request):

    if(request.method=="POST"):
        print(request.POST)
        # reason_for_removal = request.POST.get('reason_for_removal', False)
        requestobj=delete_product_list.objects.create(supplier_username=request.user.username,product_sku=request.POST['product_sku'],product_name=request.POST['product_name'],product_price=request.POST['product_price'],product_description=request.POST['product_description'],reason_for_removal=request.POST['reason_for_removal'])
        #messages.info(request, "Your request has been sent!")
#         messages.info(request, "Your Request has Sent!!")
    return render(request, 'dashboard/messagedisplay.html')

def pending_orders(request):


    x = User.objects.get(username=request.user.username)
    y=Supplier.objects.get(supplier_details=x)
    print(y.store_description)
    z = Order.objects.filter(supplier = y).filter(is_completed=False).filter(is_refunded=False)
    print(z)

    if z.exists():

        return render(request, 'dashboard/pending_orders.html', {'z':z})
    else:
            messages.info(request, "You have not recieved any orders as of now!")
            return render(request, 'dashboard/pending_orders.html')




def order_summary(request, pk):
    #    x = User.objects.get(username=request.user.username)
    #    y=Supplier.objects.get(supplier_details=x)
    #    print(y.store_description)
        z = Order.objects.get(referral_id = pk)
    #    y = Supplier.objects.get( supplier_details.username=z.user.username)
    #    print(y)
        print(z.referral_id)
        args={ 'z':z}



        return render(request, 'dashboard/order_summary.html', args )


def order_status(request, pk):

    supplier_info = Supplier.objects.get(supplier_details=request.user)
    if(request.method == "POST"):
        z= Order.objects.get(referral_id = pk)
        z.is_approved = True
        z.save()
    return render(request, 'dashboard/supplier_index.html', {'supplier_info':supplier_info})

def ship_status(request, pk):

    supplier_info = Supplier.objects.get(supplier_details=request.user)
    if(request.method == "POST"):
        z= Order.objects.get(referral_id = pk)
        z.is_shipped = True
        z.save()
    return render(request, 'dashboard/supplier_index.html', {'supplier_info':supplier_info})

def refunds(request):
    ref = []
    x = User.objects.get(username=request.user.username)
    y=Supplier.objects.get(supplier_details=x)
    z=Refunds.objects.filter(supplier = y)
    print(z)
    for m in z:
        ref.append(m)
        print(ref)
    #    print(prods)

    #print(z)

    return render(request, 'dashboard/refunds.html', {'ref':ref})

def refunds_summary(request, pk):

        z = Refunds.objects.get(refund_amount = pk)

        print(z.refund_amount)

        return render(request, 'dashboard/refunds_summary.html', {'z':z})

def approved(request):
    if request.method=='POST' and 'upload' in request.POST:
        data=addproductlist.objects.get(id=int(request.POST['upload']))
        x=User.objects.get(username=data.supplier_username)
        y=Supplier.objects.get(supplier_details=x)
        addproductlist.objects.get(id=int(request.POST['upload'])).delete()
        productdata=Product.objects.create(product_name=data.product_name,description=data.product_description,product_sku=data.product_sku,product_price=data.product_price,
                                            category="Not Added!",supplier=y)

        addproductdata=addproductlist.objects.filter(is_approved=True,supplier_username=request.user.username)
        deleteproductdata=delete_product_list.objects.filter(is_approved=True,supplier_username=request.user.username)

        return render(request,'dashboard/approvedlist.html',{'addproductdata':addproductdata,'deleteproductdata':deleteproductdata})

    elif request.method=='POST' and 'delete' in request.POST:
        data=delete_product_list.objects.get(id=int(request.POST['delete']))

        x=User.objects.get(username=data.supplier_username)
        y=Supplier.objects.get(supplier_details=x)

        data=delete_product_list.objects.get(id=int(request.POST['delete']))
        Product.objects.get(product_name=data.product_name,
                            # description=data.product_description,
                            product_sku=data.product_sku,product_price=data.product_price,supplier=y).delete()
        delete_product_list.objects.get(id=int(request.POST['delete'])).delete()
        addproductdata=addproductlist.objects.filter(is_approved=True,supplier_username=request.user.username)
        deleteproductdata=delete_product_list.objects.filter(is_approved=True,supplier_username=request.user.username)

        return render(request,'dashboard/approvedlist.html',{'addproductdata':addproductdata,'deleteproductdata':deleteproductdata})

    else:
        addproductdata=addproductlist.objects.filter(is_approved=True,supplier_username=request.user.username)
        deleteproductdata=delete_product_list.objects.filter(is_approved=True,supplier_username=request.user.username)
        return render(request,'dashboard/approvedlist.html',{'addproductdata':addproductdata,'deleteproductdata':deleteproductdata})
