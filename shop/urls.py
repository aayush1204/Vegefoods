from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),

    path('product-single/<int:q>',views.product_single,name='product_single'),
    path('home/<int:q>',views.add_cart,name='add_to_cart'),
    path('home/myorders', views.myorders,name='myorders'),
    path('home/myorders/refunds/<int:x>', views.refund,name='refund'),
    path('home/myorders/ordertrack/<int:x>', views.track,name='track'),

    path('home/myrefunds', views.myrefunds,name='myrefunds'),
    path('home/contact', views.contact,name='contact'),
    path('cart/', views.cart_view,name='cart'),
    path('cart/<int:p>', views.delete_cart,name='delete_cart_item'),
    path('shop/', views.shop_view,name='shop'),
    path('shop/<slug:name>',views.filter,name='filter'),
    path('cart/checkout', views.checkout_view,name='checkout'),
    path('cart/checkout/placed', views.order_place, name='order_place'),
]
