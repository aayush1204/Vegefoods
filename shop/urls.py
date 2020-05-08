from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('/product-single',views.product_single,name='product_single'),
]
