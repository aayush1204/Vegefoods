from django.shortcuts import render,redirect
import requests
from .forms import loginform
from supplier.models import Product
from shop.models import Supplier
from django.contrib.auth.models import User
from django.http import HttpResponse
from shop.models import Order
from .models import adminmodel,addproductlist
# Create your views here.

def homepage(request):
    # currentuser = request.COOKIES['username']

    return render(request,'admin/dash.html',)


# def login(request):
#     # print(request.method)
#     print('login')
#     if request.method=='GET':
#         print('login GET')
#         forminput=loginform()
#         return render(request,'adminlogin.html',{'forminput':forminput})
#     elif request.method=='POST':
#         currentuser=""
#         print('login POST')
#         forminput=loginform(request.POST)
#         if forminput.is_valid():
#             username=forminput.cleaned_data['username']
#             password=forminput.cleaned_data['password']
#         print(username)
#         print(password)
#         try:
#
#             admindata=adminmodel.objects.get(username=username)
#             # print(admindata.username)
#             # print(admindata.password)
#             # print(admindata.password==password)
#             if admindata.password==password:
#                     # print('yes')
#                     currentuser=admindata.username
#                     # return HttpResponse('yes')
#                     name='admindash.html'
#             else:
#                 name='adminlogin.html'
#                     # return render(request,'admindash.html',{'currentuser':currentuser})
#
#         except :
#             name='adminlogin.html'
#             message='Username or Password was incorrect'
#
#         message='Username or Password was incorrect'
#         # print(name)
#         # return HttpResponse(message)
#         # return render(request,'adminlogin.html',{'forminput':forminput,'message':message})
#         response=render(request,name,{'forminput':forminput,'message':message,'currentuser':currentuser})
#         response.set_cookie('username',username)
#         return response
        # return render(request,name,{'forminput':forminput,'message':message,'currentuser':currentuser})
def supplierslist(request):
    print('supplierslist')
    # currentuser = request.COOKIES['username']
    suppdata=Supplier.objects.all()
    # print(type(suppdata))
    return render(request,'admin/supplierslist.html',{'suppdata':suppdata})
def requestslist(request):
    currentuser = request.COOKIES['username']

    print('requestslist')
    return render(request,'admin/requestslist.html',{'currentuser':currentuser})

def complaintslist(request):
    currentuser = request.COOKIES['username']

    print('complaintslist')
    return render(request,'complaintslist.html',{'currentuser':currentuser})
def refundslist(request):
    currentuser = request.COOKIES['username']

    print('refundslist')
    return render(request,'admin/refundslist.html',{'currentuser':currentuser})
def orderslist(request):
    print('orderslist')
    currentuser = request.COOKIES['username']

    orderdata=Order.objects.filter(is_completed=False)
    print(type(orderdata))
    return render(request,'orderslist.html',{'orderdata':orderdata,'currentuser':currentuser})

def approvallist(request):
    print('approvallist')
    # currentuser = request.COOKIES['username']

    approvaldata=Supplier.objects.filter(is_approved=False)
    print(approvaldata)
    return render(request,'admin/approvallist.html',{'approvaldata':approvaldata})

def deleteproduct(request):
    print('deleteproduct')
    currentuser = request.COOKIES['username']

    return render(request,'deleteproduct.html',{'currentuser':currentuser})

def newproduct(request):
    if request.method=='GET':
        print('newproduct')
        # currentuser = request.COOKIES['username']
        addproddata=addproductlist.objects.all()
        return render(request,'admin/newproduct.html',{'addproddata':addproddata})
    elif request.method=='POST':

        data=addproductlist.objects.get(id=int(request.POST['clicked']))
        x=User.objects.get(username=data.username)
        y=Supplier.objects.get(supplier_details=x)
        addproductlist.objects.get(id=request.POST['clicked']).delete()
        addproductdata=Product.objects.create(product_name=data.product_name,product_description=data.product_description,product_sku=data.product_sku,product_price=data.product_price,
                                                category="Not Added!",supplier=x)

        addproddata=addproductlist.objects.all()
        return render(request,'admin/newproduct.html',{'addproddata':addproddata})
def logout(request):

    response= redirect('/office',{'message':'You have successfully logged out'})
    response.delete_cookie('username')
    return response
