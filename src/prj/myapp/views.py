from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.db.models import F
from .models import *

# ====================
# Home View
# ====================
def home_view(request):
    return render(request, 'base.html')


# ====================
# Wilaya Views
# ====================
class WilayaListView(ListView):
    model = Wilaya
    template_name = 'wilaya-list.html'
    context_object_name = 'wilayas'

class WilayaDetailView(DetailView):
    model = Wilaya
    template_name = 'wilaya-detail.html'

class WilayaCreateView(CreateView):
    model = Wilaya
    fields = '__all__'
    template_name = 'wilaya-form.html'
    success_url = reverse_lazy('wilaya-list')

class WilayaUpdateView(UpdateView):
    model = Wilaya
    fields = '__all__'
    template_name = 'wilaya-form.html'
    success_url = reverse_lazy('wilaya-list')

class WilayaDeleteView(DeleteView):
    model = Wilaya
    template_name = 'wilaya-confirm-delete.html'
    success_url = reverse_lazy('wilaya-list')


# ====================
# Moughataa Views
# ====================
class MoughataaListView(ListView):
    model = Moughataa
    template_name = 'moughataa-list.html'
    context_object_name = 'moughataas'

class MoughataaDetailView(DetailView):
    model = Moughataa
    template_name = 'moughataa-detail.html'

class MoughataaCreateView(CreateView):
    model = Moughataa
    fields = '__all__'
    template_name = 'moughataa-form.html'
    success_url = reverse_lazy('moughataa-list')

class MoughataaUpdateView(UpdateView):
    model = Moughataa
    fields = '__all__'
    template_name = 'moughataa-form.html'
    success_url = reverse_lazy('moughataa-list')

class MoughataaDeleteView(DeleteView):
    model = Moughataa
    template_name = 'moughataa-confirm-delete.html'
    success_url = reverse_lazy('moughataa-list')


# ====================
# Commune Views
# ====================
class CommuneListView(ListView):
    model = Commune
    template_name = 'commune-list.html'
    context_object_name = 'communes'

class CommuneDetailView(DetailView):
    model = Commune
    template_name = 'commune-detail.html'

class CommuneCreateView(CreateView):
    model = Commune
    fields = '__all__'
    template_name = 'commune-form.html'
    success_url = reverse_lazy('commune-list')

class CommuneUpdateView(UpdateView):
    model = Commune
    fields = '__all__'
    template_name = 'commune-form.html'
    success_url = reverse_lazy('commune-list')

class CommuneDeleteView(DeleteView):
    model = Commune
    template_name = 'commune-confirm-delete.html'
    success_url = reverse_lazy('commune-list')


# ====================
# Point of Sale Views
# ====================
class PointOfSaleListView(ListView):
    model = PointOfSale
    template_name = 'pointofsale-list.html'
    context_object_name = 'point_of_sales'


class PointOfSaleDetailView(DetailView):
    model = PointOfSale
    template_name = 'pointofsale-detail.html'
    context_object_name = 'pointVente'


class PointOfSaleCreateView(CreateView):
    model = PointOfSale
    fields = ['code', 'type', 'gps_lat', 'gps_lon', 'commune']
    template_name = 'pointofsale-form.html'
    success_url = reverse_lazy('pointofsale-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Récupérer les types distincts pour la liste déroulante
        context['point_of_sale_types'] = PointOfSale.objects.values_list('type', flat=True).distinct()
        return context



class PointOfSaleUpdateView(UpdateView):
    model = PointOfSale
    fields = ['code', 'type', 'gps_lat', 'gps_lon', 'commune']
    template_name = 'pointofsale-form.html'
    success_url = reverse_lazy('pointofsale-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['point_of_sale_types'] = PointOfSale.objects.values_list('type', flat=True).distinct()
        return context


class PointOfSaleDeleteView(DeleteView):
    model = PointOfSale
    template_name = 'pointofsale-confirm-delete.html'
    success_url = reverse_lazy('pointofsale-list')

# ====================
# Product Views
# ====================
class ProductListView(ListView):
    model = Product
    template_name = 'product-list.html'
    context_object_name = 'products'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product-detail.html'

class ProductCreateView(CreateView):
    model = Product
    fields = ['code', 'name', 'description', 'unit_measure', 'product_type']
    template_name = 'product-form.html'
    success_url = reverse_lazy('product-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Passer tous les types de produits au template
        context['product_types'] = ProductType.objects.all()
        return context


class ProductUpdateView(UpdateView):
    model = Product
    fields = ['code', 'name', 'description', 'unit_measure', 'product_type']
    template_name = 'product-form.html'
    success_url = reverse_lazy('product-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_types'] = ProductType.objects.all()  # Correctement indenté
        return context

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product-confirm-delete.html'
    success_url = reverse_lazy('product-list')


# ====================
# Product Price Views
# ====================
class ProductPriceListView(ListView):
    model = ProductPrice
    template_name = 'productprice-list.html'
    context_object_name = 'product_prices'

class ProductPriceDetailView(DetailView):
    model = ProductPrice
    template_name = 'productprice-detail.html'

class ProductPriceCreateView(CreateView):
    model = ProductPrice
    fields = '__all__'
    template_name = 'productprice-form.html'
    success_url = reverse_lazy('productprice-list')

class ProductPriceUpdateView(UpdateView):
    model = ProductPrice
    fields = '__all__'
    template_name = 'productprice-form.html'
    success_url = reverse_lazy('productprice-list')

class ProductPriceDeleteView(DeleteView):
    model = ProductPrice
    template_name = 'productprice-confirm-delete.html'
    success_url = reverse_lazy('productprice-list')


# ====================
# Cart Views
# ====================
class CartListView(ListView):
    model = Cart
    template_name = 'cart-list.html'
    context_object_name = 'carts'

class CartDetailView(DetailView):
    model = Cart
    template_name = 'cart-detail.html'

class CartCreateView(CreateView):
    model = Cart
    fields = '__all__'
    template_name = 'cart-form.html'
    success_url = reverse_lazy('cart-list')

class CartUpdateView(UpdateView):
    model = Cart
    fields = '__all__'
    template_name = 'cart-form.html'
    success_url = reverse_lazy('cart-list')

class CartDeleteView(DeleteView):
    model = Cart
    template_name = 'cart-confirm-delete.html'
    success_url = reverse_lazy('cart-list')


# ====================
# Cart Products Views
# ====================
class CartProductsListView(ListView):
    model = CartProducts
    template_name = 'cartproducts-list.html'
    context_object_name = 'cart_products'

class CartProductsDetailView(DetailView):
    model = CartProducts
    template_name = 'cartproducts-detail.html'

class CartProductsCreateView(CreateView):
    model = CartProducts
    fields = '__all__'
    template_name = 'cartproducts-form.html'
    success_url = reverse_lazy('cartproducts-list')

class CartProductsUpdateView(UpdateView):
    model = CartProducts
    fields = '__all__'
    template_name = 'cartproducts-form.html'
    success_url = reverse_lazy('cartproducts-list')

class CartProductsDeleteView(DeleteView):
    model = CartProducts
    template_name = 'cartproducts-confirm-delete.html'
    success_url = reverse_lazy('cartproducts-list')
