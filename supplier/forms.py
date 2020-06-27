from django.forms import ModelForm
from shop.models import Product
from admindashboard.models import addproductlist


class AddProductForm(ModelForm):
    class Meta:

        model = addproductlist
        fields = '__all__'
        exclude = ['discount_price','discount_percent','discount_applied','is_approved','out_of_stock', 'supplier']
