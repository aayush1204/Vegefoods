from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('product-single/<slug:name>',views.product_single,name='product_single'),

]
