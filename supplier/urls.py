from django.urls import path
from . import views

urlpatterns = [

        path('supplier_register', views.supplier_register, name='supplier_register'),
        path('home/<str:pk>', views.home, name='home'),
        path('login', views.login, name='login'),
        path('supplier_login', views.supplier_login, name='supplier_login'),
        path('products/<str:pk>/', views.products, name='products'),
        path('add/addnew', views.addnew, name='addnew'),
        path('add/<str:pk>', views.add, name='add'),
        path('delete/<str:pk>', views.delete, name='delete'),
        path('delete/delete_existing', views.delete_existing, name='delete_existing'),
        path('home/<str:pk>', views.home, name='home'),
]
