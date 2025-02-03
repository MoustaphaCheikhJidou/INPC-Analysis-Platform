# urls.py

from django.urls import path
from .views import (
    home_view,
    commune_list_view,import_point_of_sale_view,import_productprice_view, productprice_list_view,
    import_data_view,import_product_view,import_cartproducts_view,cartproducts_list_view,
    point_of_sale_list_view, point_of_sale_detail, point_of_sale_create, point_of_sale_update, point_of_sale_delete,
    product_list_view, product_detail, product_create, product_update, product_delete,
    productprice_detail, productprice_create, productprice_update, productprice_delete,
    cart_list_view, import_cart_view, cart_detail, cart_create, cart_update, cart_delete,
    cartproducts_detail, cartproducts_create, cartproducts_update, cartproducts_delete,
    producttype_list_view, import_producttype_view,
    producttype_detail, producttype_create, producttype_update, producttype_delete,
)
from . import views

urlpatterns = [
    path('', home_view, name='home'),
    path('communes/', commune_list_view, name='commune-list'),
    path('communes/import/', import_data_view, name='import_data'),
    # Point of Sale URLs
    path('points-of-sale/', point_of_sale_list_view, name='pointofsale-list'),
    path("points-of-sale/import/", import_point_of_sale_view, name="pointofsale-import"),
    path('points-of-sale/create/', point_of_sale_create, name='pointofsale-create'),
    path('points-of-sale/<int:pk>/', point_of_sale_detail, name='pointofsale-detail'),
    path('points-of-sale/<int:pk>/update/', point_of_sale_update, name='pointofsale-update'),
    path('points-of-sale/<int:pk>/delete/', point_of_sale_delete, name='pointofsale-delete'),

    # Product URLs
    path('product/', product_list_view, name='product-list'),
    path("product/import/", import_product_view, name="product-import"),
    path('product/create/', product_create, name='product-create'),
    path('product/<int:pk>/', product_detail, name='product-detail'),
    path('product/<int:pk>/update/', product_update, name='product-update'),
    path('product/<int:pk>/delete/', product_delete, name='product-delete'),

    # Product Price URLs
    path('product-price/', productprice_list_view, name='productprice-list'),
    path("product-price/import/", import_productprice_view, name="productprice-import"),
        path('product-price/create/', productprice_create, name='productprice-create'),
    path('product-price/<int:pk>/', productprice_detail, name='productprice-detail'),
    path('product-price/<int:pk>/update/', productprice_update, name='productprice-update'),
    path('product-price/<int:pk>/delete/', productprice_delete, name='productprice-delete'),

    # Cart URLs
    path('cart/', cart_list_view, name='cart-list'),
    path('cart/import/', import_cart_view, name='cart-import'),
        path('cart/create/', cart_create, name='cart-create'),
    path('cart/<int:pk>/', cart_detail, name='cart-detail'),
    path('cart/<int:pk>/update/', cart_update, name='cart-update'),
    path('cart/<int:pk>/delete/', cart_delete, name='cart-delete'),

    # Cart Products URLs
    path('cart-products/', cartproducts_list_view, name='cartproducts-list'),
    path('cart-products/import/', import_cartproducts_view, name='cartproducts-import'),
        path('cart-products/create/', cartproducts_create, name='cartproducts-create'),
    path('cart-products/<int:pk>/', cartproducts_detail, name='cartproducts-detail'),
    path('cart-products/<int:pk>/update/', cartproducts_update, name='cartproducts-update'),
    path('cart-products/<int:pk>/delete/', cartproducts_delete, name='cartproducts-delete'),
    
     # Product Type URLs
    path('producttypes/', producttype_list_view, name='producttype-list'),
    path('producttypes/import/', import_producttype_view, name='producttype-import'),
    path('producttypes/<int:pk>/', producttype_detail, name='producttype-detail'),
    path('producttypes/create/', producttype_create, name='producttype-create'),
    path('producttypes/<int:pk>/update/', producttype_update, name='producttype-update'),
    path('producttypes/<int:pk>/delete/', producttype_delete, name='producttype-delete'),

    #API
 path('api/communes/geojson/', views.CommuneGeoList.as_view(), name='commune-geojson-api'),
    path('api/wilayas/geojson/', views.WilayaGeoList.as_view(), name='wilaya-geojson-api'),
        path('api/moughataas/geojson/', views.MoughataaGeoList.as_view(), name='moughataa-geojson'),

    path('api/points-of-sale/', views.PointOfSaleList.as_view(), name='pointofsale-list-api'),
    path('api/products/', views.ProductList.as_view(), name='product-list-api'),
    path('api/product-prices/', views.ProductPriceList.as_view(), name='productprice-list-api'),
    path('mrmap/', views.mrmap_view, name='mrmap'),
    path('calculate-inpc/', views.calculate_inpc, name='calculate-inpc'),
    path('debug-geometries/', views.debug_geometries, name='debug-geometries'),
    path('collect-data/', views.data_collection_view, name='data-collection'),
    path('generate_report_pdf/', views.generate_report_pdf, name='generate_report_pdf'),
]  