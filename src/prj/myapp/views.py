from django.shortcuts import render  
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy

from . import models
from .models import Product, Wilaya, Moughataa, Commune, PointOfSale, ProductPrice, Cart, CartProducts

def home_view(request):
    return render(request, 'base.html')



# ProductType Views
class ProductTypeListView(ListView):
    model = models


class ProductTypeDetailView(DetailView):
    model = models


class ProductTypeCreateView(CreateView):
    model = models
    fields = '__all__'
    success_url = reverse_lazy('producttype_list')


class ProductTypeDeleteView(DeleteView):
    model = models
    success_url = reverse_lazy('producttype_list')


class ProductTypeUpdateView(UpdateView):
    model = models
    fields = '__all__'
    success_url = reverse_lazy('producttype_list')


# Product Views
class ProductListView(ListView):
    model = Product


class ProductDetailView(DetailView):
    model = Product


class ProductCreateView(CreateView):
    model = Product
    fields = '__all__'
    success_url = reverse_lazy('product_list')


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('product_list')


class ProductUpdateView(UpdateView):
    model = Product
    fields = '__all__'
    success_url = reverse_lazy('product_list')


class WilayaListView(ListView):
    model = Wilaya
    template_name = 'wilaya_list.html'  # Specify the template explicitly


class WilayaDetailView(DetailView):
    model = Wilaya
    template_name = 'wilaya_detail.html'  # Specify the template explicitly


class WilayaCreateView(CreateView):
    model = Wilaya
    fields = '__all__'
    template_name = 'wilaya_form.html'  # Specify the template explicitly
    success_url = reverse_lazy('wilaya_list')


class WilayaUpdateView(UpdateView):
    model = Wilaya
    fields = '__all__'
    template_name = 'wilaya_form.html'  # Specify the template explicitly
    success_url = reverse_lazy('wilaya_list')


class WilayaDeleteView(DeleteView):
    model = Wilaya
    template_name = 'wilaya_confirm_delete.html'  # Specify the template explicitly
    success_url = reverse_lazy('wilaya_list')


# Moughataa Views
class MoughataaListView(ListView):
    model = Moughataa


class MoughataaDetailView(DetailView):
    model = Moughataa


class MoughataaCreateView(CreateView):
    model = Moughataa
    fields = '__all__'
    success_url = reverse_lazy('moughataa_list')


class MoughataaDeleteView(DeleteView):
    model = Moughataa
    success_url = reverse_lazy('moughataa_list')


class MoughataaUpdateView(UpdateView):
    model = Moughataa
    fields = '__all__'
    success_url = reverse_lazy('moughataa_list')


# Commune Views
class CommuneListView(ListView):
    model = Commune


class CommuneDetailView(DetailView):
    model = Commune


class CommuneCreateView(CreateView):
    model = Commune
    fields = '__all__'
    success_url = reverse_lazy('commune_list')


class CommuneDeleteView(DeleteView):
    model = Commune
    success_url = reverse_lazy('commune_list')


class CommuneUpdateView(UpdateView):
    model = Commune
    fields = '__all__'
    success_url = reverse_lazy('commune_list')


# PointOfSale Views
class PointOfSaleListView(ListView):
    model = PointOfSale


class PointOfSaleDetailView(DetailView):
    model = PointOfSale


class PointOfSaleCreateView(CreateView):
    model = PointOfSale
    fields = '__all__'
    success_url = reverse_lazy('pointofsale_list')


class PointOfSaleDeleteView(DeleteView):
    model = PointOfSale
    success_url = reverse_lazy('pointofsale_list')


class PointOfSaleUpdateView(UpdateView):
    model = PointOfSale
    fields = '__all__'
    success_url = reverse_lazy('pointofsale_list')


# ProductPrice Views
class ProductPriceListView(ListView):
    model = ProductPrice


class ProductPriceDetailView(DetailView):
    model = ProductPrice


class ProductPriceCreateView(CreateView):
    model = ProductPrice
    fields = '__all__'
    success_url = reverse_lazy('productprice_list')


class ProductPriceDeleteView(DeleteView):
    model = ProductPrice
    success_url = reverse_lazy('productprice_list')


class ProductPriceUpdateView(UpdateView):
    model = ProductPrice
    fields = '__all__'
    success_url = reverse_lazy('productprice_list')


# Cart Views
class CartListView(ListView):
    model = Cart


class CartDetailView(DetailView):
    model = Cart


class CartCreateView(CreateView):
    model = Cart
    fields = '__all__'
    success_url = reverse_lazy('cart_list')


class CartDeleteView(DeleteView):
    model = Cart
    success_url = reverse_lazy('cart_list')


class CartUpdateView(UpdateView):
    model = Cart
    fields = '__all__'
    success_url = reverse_lazy('cart_list')


# CartProducts Views
class CartProductsListView(ListView):
    model = CartProducts


class CartProductsDetailView(DetailView):
    model = CartProducts


class CartProductsCreateView(CreateView):
    model = CartProducts
    fields = '__all__'
    success_url = reverse_lazy('cartproducts_list')


class CartProductsDeleteView(DeleteView):
    model = CartProducts
    success_url = reverse_lazy('cartproducts_list')


class CartProductsUpdateView(UpdateView):
    model = CartProducts
    fields = '__all__'
    success_url = reverse_lazy('cartproducts_list')
