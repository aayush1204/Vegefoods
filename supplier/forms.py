from django.forms import ModelForm
from shop.models import Product
from admindashboard.models import addproductlist
from django import forms

class AddProductForm(ModelForm):
    class Meta:

        model = addproductlist
        fields = '__all__'
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control'}),
            'product_description': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'product_sku': forms.TextInput(attrs={'class': 'form-control'}),
            'product_price': forms.TextInput(attrs={'class': 'form-control'}),
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'supplier_username': forms.TextInput(attrs={'class': 'form-control'}),
            # 'videofile': forms.FileInput(attrs={'class': 'form-control'}),
            
        }
        exclude = ['discount_price','discount_percent','discount_applied','is_approved','out_of_stock']
