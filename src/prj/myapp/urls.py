from django.urls import path
from .views import (
    home_view,
    ProductTypeListView, ProductTypeDetailView, ProductTypeCreateView, ProductTypeUpdateView, ProductTypeDeleteView,
    ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView,
    WilayaListView, WilayaDetailView, WilayaCreateView, WilayaUpdateView, WilayaDeleteView,
    MoughataaListView, MoughataaDetailView, MoughataaCreateView, MoughataaUpdateView, MoughataaDeleteView,
    CommuneListView, CommuneDetailView, CommuneCreateView, CommuneUpdateView, CommuneDeleteView,
    PointOfSaleListView, PointOfSaleDetailView, PointOfSaleCreateView, PointOfSaleUpdateView, PointOfSaleDeleteView,
    ProductPriceListView, ProductPriceDetailView, ProductPriceCreateView, ProductPriceUpdateView, ProductPriceDeleteView,
    CartListView, CartDetailView, CartCreateView, CartUpdateView, CartDeleteView,
    CartProductsListView, CartProductsDetailView, CartProductsCreateView, CartProductsUpdateView, CartProductsDeleteView,
)

urlpatterns = [
    path('wilaya/', WilayaListView.as_view(), name='wilaya_list'),
    path('wilaya/create/', WilayaCreateView.as_view(), name='wilaya_create'),  # Ensure this exists
    path('', home_view, name='home'),
    
    # ProductType URLs
    path('producttype/', ProductTypeListView.as_view(), name='producttype_list'),
    path('producttype/<int:pk>/', ProductTypeDetailView.as_view(), name='producttype_detail'),
    path('producttype/create/', ProductTypeCreateView.as_view(), name='producttype_create'),
    path('producttype/<int:pk>/update/', ProductTypeUpdateView.as_view(), name='producttype_update'),
    path('producttype/<int:pk>/delete/', ProductTypeDeleteView.as_view(), name='producttype_delete'),

    # Product URLs
    path('product/', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),

    # Wilaya URLs
    path('wilaya/', WilayaListView.as_view(), name='wilaya_list'),
    path('wilaya/<int:pk>/', WilayaDetailView.as_view(), name='wilaya_detail'),
    path('wilaya/create/', WilayaCreateView.as_view(), name='wilaya_create'),
    path('wilaya/<int:pk>/update/', WilayaUpdateView.as_view(), name='wilaya_update'),
    path('wilaya/<int:pk>/delete/', WilayaDeleteView.as_view(), name='wilaya_delete'),

    # Moughataa URLs
    path('moughataa/', MoughataaListView.as_view(), name='moughataa_list'),
    path('moughataa/<int:pk>/', MoughataaDetailView.as_view(), name='moughataa_detail'),
    path('moughataa/create/', MoughataaCreateView.as_view(), name='moughataa_create'),
    path('moughataa/<int:pk>/update/', MoughataaUpdateView.as_view(), name='moughataa_update'),
    path('moughataa/<int:pk>/delete/', MoughataaDeleteView.as_view(), name='moughataa_delete'),

    # Commune URLs
    path('commune/', CommuneListView.as_view(), name='commune_list'),
    path('commune/<int:pk>/', CommuneDetailView.as_view(), name='commune_detail'),
    path('commune/create/', CommuneCreateView.as_view(), name='commune_create'),
    path('commune/<int:pk>/update/', CommuneUpdateView.as_view(), name='commune_update'),
    path('commune/<int:pk>/delete/', CommuneDeleteView.as_view(), name='commune_delete'),

    # PointOfSale URLs
    path('pointofsale/', PointOfSaleListView.as_view(), name='pointofsale_list'),
    path('pointofsale/<int:pk>/', PointOfSaleDetailView.as_view(), name='pointofsale_detail'),
    path('pointofsale/create/', PointOfSaleCreateView.as_view(), name='pointofsale_create'),
    path('pointofsale/<int:pk>/update/', PointOfSaleUpdateView.as_view(), name='pointofsale_update'),
    path('pointofsale/<int:pk>/delete/', PointOfSaleDeleteView.as_view(), name='pointofsale_delete'),

    # ProductPrice URLs
    path('productprice/', ProductPriceListView.as_view(), name='productprice_list'),
    path('productprice/<int:pk>/', ProductPriceDetailView.as_view(), name='productprice_detail'),
    path('productprice/create/', ProductPriceCreateView.as_view(), name='productprice_create'),
    path('productprice/<int:pk>/update/', ProductPriceUpdateView.as_view(), name='productprice_update'),
    path('productprice/<int:pk>/delete/', ProductPriceDeleteView.as_view(), name='productprice_delete'),

    # Cart URLs
    path('cart/', CartListView.as_view(), name='cart_list'),
    path('cart/<int:pk>/', CartDetailView.as_view(), name='cart_detail'),
    path('cart/create/', CartCreateView.as_view(), name='cart_create'),
    path('cart/<int:pk>/update/', CartUpdateView.as_view(), name='cart_update'),
    path('cart/<int:pk>/delete/', CartDeleteView.as_view(), name='cart_delete'),

    # CartProducts URLs
    path('cartproducts/', CartProductsListView.as_view(), name='cartproducts_list'),
    path('cartproducts/<int:pk>/', CartProductsDetailView.as_view(), name='cartproducts_detail'),
    path('cartproducts/create/', CartProductsCreateView.as_view(), name='cartproducts_create'),
    path('cartproducts/<int:pk>/update/', CartProductsUpdateView.as_view(), name='cartproducts_update'),
    path('cartproducts/<int:pk>/delete/', CartProductsDeleteView.as_view(), name='cartproducts_delete'),
]