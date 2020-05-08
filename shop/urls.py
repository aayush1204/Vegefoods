from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    
    path('product-single/<slug:name>',views.product_single,name='product_single'),
    path('home/<slug:name>',views.add_cart,name='add_to_cart'),
    path('cart/', views.cart_view,name='cart')

]
