# forms.py
from django import forms
from .models import ProductType, Product, ProductPrice, Cart, CartProducts, PointOfSale

class ProductTypeForm(forms.ModelForm):
    class Meta:
        model = ProductType
        fields = '__all__'

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class ProductPriceForm(forms.ModelForm):
    class Meta:
        model = ProductPrice
        fields = '__all__'

class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = '__all__'

class CartProductsForm(forms.ModelForm):
    class Meta:
        model = CartProducts
        fields = '__all__'

class PointOfSaleForm(forms.ModelForm):
    class Meta:
        model = PointOfSale
        fields = '__all__'