from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    
    path('product-single/<slug:name>',views.product_single,name='product_single'),
    path('home/<slug:name>',views.add_cart,name='add_to_cart'),
    path('cart/', views.cart_view,name='cart'),
    path('shop/', views.shop_view,name='shop'),
    path('shop/<slug:name>',views.filter,name='filter'),
    path('cart/checkout', views.checkout_view,name='checkout'),
    path('cart/checkout/placed', views.address, name='address'),
]
