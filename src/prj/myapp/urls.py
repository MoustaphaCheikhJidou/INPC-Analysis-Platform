from django.urls import path
from .views import (
    home_view,
    WilayaListView, WilayaDetailView, WilayaCreateView, WilayaUpdateView, WilayaDeleteView,
    MoughataaListView, MoughataaDetailView, MoughataaCreateView, MoughataaUpdateView, MoughataaDeleteView,
    CommuneListView, CommuneDetailView, CommuneCreateView, CommuneUpdateView, CommuneDeleteView,
    PointOfSaleListView, PointOfSaleDetailView, PointOfSaleCreateView, PointOfSaleUpdateView, PointOfSaleDeleteView,
    ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView,
    ProductPriceListView, ProductPriceDetailView, ProductPriceCreateView, ProductPriceUpdateView, ProductPriceDeleteView,
    CartListView, CartDetailView, CartCreateView, CartUpdateView, CartDeleteView,
    CartProductsListView, CartProductsDetailView, CartProductsCreateView, CartProductsUpdateView, CartProductsDeleteView,
)


urlpatterns = [
    path('', home_view, name='home'),

    # Wilaya URLs
    path('wilaya/', WilayaListView.as_view(), name='wilaya-list'),
    path('wilaya/create/', WilayaCreateView.as_view(), name='wilaya-create'),
    path('wilaya/<int:pk>/', WilayaDetailView.as_view(), name='wilaya-detail'),
    path('wilaya/<int:pk>/update/', WilayaUpdateView.as_view(), name='wilaya-update'),
    path('wilaya/<int:pk>/delete/', WilayaDeleteView.as_view(), name='wilaya-delete'),

    # Moughataa URLs
    path('moughataa/', MoughataaListView.as_view(), name='moughataa-list'),
    path('moughataa/create/', MoughataaCreateView.as_view(), name='moughataa-create'),
    path('moughataa/<int:pk>/', MoughataaDetailView.as_view(), name='moughataa-detail'),
    path('moughataa/<int:pk>/update/', MoughataaUpdateView.as_view(), name='moughataa-update'),
    path('moughataa/<int:pk>/delete/', MoughataaDeleteView.as_view(), name='moughataa-delete'),

    # Commune URLs
    path('commune/', CommuneListView.as_view(), name='commune-list'),
    path('commune/create/', CommuneCreateView.as_view(), name='commune-create'),
    path('commune/<int:pk>/', CommuneDetailView.as_view(), name='commune-detail'),
    path('commune/<int:pk>/update/', CommuneUpdateView.as_view(), name='commune-update'),
    path('commune/<int:pk>/delete/', CommuneDeleteView.as_view(), name='commune-delete'),

    # Point of Sale URLs
    path('point-of-sale/', PointOfSaleListView.as_view(), name='pointofsale-list'),
    path('point-of-sale/create/', PointOfSaleCreateView.as_view(), name='pointofsale-create'),
    path('point-of-sale/<int:pk>/', PointOfSaleDetailView.as_view(), name='pointofsale-detail'),
    path('point-of-sale/<int:pk>/update/', PointOfSaleUpdateView.as_view(), name='pointofsale-update'),
    path('point-of-sale/<int:pk>/delete/', PointOfSaleDeleteView.as_view(), name='pointofsale-delete'),

    # Product URLs
    path('product/', ProductListView.as_view(), name='product-list'),
    path('product/create/', ProductCreateView.as_view(), name='product-create'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),

    # Product Price URLs
    path('product-price/', ProductPriceListView.as_view(), name='productprice-list'),
    path('product-price/create/', ProductPriceCreateView.as_view(), name='productprice-create'),
    path('product-price/<int:pk>/', ProductPriceDetailView.as_view(), name='productprice-detail'),
    path('product-price/<int:pk>/update/', ProductPriceUpdateView.as_view(), name='productprice-update'),
    path('product-price/<int:pk>/delete/', ProductPriceDeleteView.as_view(), name='productprice-delete'),

    # Cart URLs
    path('cart/', CartListView.as_view(), name='cart-list'),
    path('cart/create/', CartCreateView.as_view(), name='cart-create'),
    path('cart/<int:pk>/', CartDetailView.as_view(), name='cart-detail'),
    path('cart/<int:pk>/update/', CartUpdateView.as_view(), name='cart-update'),
    path('cart/<int:pk>/delete/', CartDeleteView.as_view(), name='cart-delete'),

    # Cart Products URLs
    path('cart-products/', CartProductsListView.as_view(), name='cartproducts-list'),
    path('cart-products/create/', CartProductsCreateView.as_view(), name='cartproducts-create'),
    path('cart-products/<int:pk>/', CartProductsDetailView.as_view(), name='cartproducts-detail'),
    path('cart-products/<int:pk>/update/', CartProductsUpdateView.as_view(), name='cartproducts-update'),
    path('cart-products/<int:pk>/delete/', CartProductsDeleteView.as_view(), name='cartproducts-delete'),
]
