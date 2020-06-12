from django.urls import path,include
from . import views

urlpatterns = [

        path('home/sell-with-us', views.sellwithus, name='sell_with_us'),
        path('home-supplier', views.supplier_login, name='supplier_login'),
        path('home', views.home, name='home'),
        path('supplier_index', views.supplier_index, name='supplier_index'),
        path('login', views.login, name='login'),

        path('products', views.products, name='products'),
        path('addnew', views.addnew, name='addnew'),
        path('add', views.add, name='add'),
        path('delete', views.delete, name='delete'),
        path('delete_existing', views.delete_existing, name='delete_existing'),
        path('pending_orders', views.pending_orders, name='pending_orders'),
        path('order_summary/<str:pk>', views.order_summary, name='order_summary'),
        path('refunds', views.refunds, name='refunds'),
        path('refunds_summary/<str:pk>', views.refunds_summary, name='refunds_summary'),
        path('order_status/<str:pk>', views.order_status, name='order_status'),
        path('ship_status/<str:pk>', views.ship_status, name='ship_status'),
        path('approved/', views.approved, name='approved'),

        # path('',include('admindashboard.urls')),

        #path('home/<str:pk>', views.home, name='home'),
]
