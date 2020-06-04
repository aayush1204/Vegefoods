from django.urls import path
from . import views
# from django.generic.views import TemplateView

urlpatterns = [
    path('',views.homepage,name='homepage'),

    path('supplierslist/',views.supplierslist,name='supplierslist'),
    path('requestslist/',views.requestslist,name='requestslist'),
    path('orderslist/',views.orderslist,name='orderslist'),
    path('refundslist/',views.refundslist,name='refundslist'),
    path('complaintslist/',views.complaintslist,name='complaintslist'),
    path('approval/',views.approvallist,name='approval'),
    path('deleteproduct/',views.deleteproduct,name='deleteproduct'),
    path('newproduct/',views.newproduct,name='newproduct'),
    path('societies/',views.societieslist,name='societies'),
    path('vouchers/',views.vouchers,name='vouchers'),

    path('viewvoucher/',views.viewvoucher,name='viewvoucher'),
    path('createvoucher/',views.createvoucher,name='createvoucher'),
    path('updatevoucher/',views.updatevoucher,name='updatevoucher'),
    path('deletevoucher/',views.deletevoucher,name='deletevoucher'),

    path('viewsocieties/',views.viewsocieties,name='viewsocieties'),
    path('createsocieties/',views.createsocieties,name='createsocieties'),
    path('updatesocieties/',views.updatesocieties,name='updatesocieties'),
    path('deletesocieties/',views.deletesocieties,name='deletesocieties'),

    # path('/supplierslist',views.supplierslist,name='supplierslist'),
    path('logout/',views.logout,name='logout'),

    # path('home/',views.homepage,name='homepage'),


]
