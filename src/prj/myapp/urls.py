from django.urls import path
from .views import (
    home_view,inpc_view,
    commune_list_view,import_point_of_sale_view,import_productprice_view, productprice_list_view,
    import_data_view,import_product_view,import_cartproducts_view,cartproducts_list_view,
    point_of_sale_list_view, PointOfSaleDetailView, PointOfSaleCreateView, PointOfSaleUpdateView, PointOfSaleDeleteView,
    product_list_view, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView,
     ProductPriceDetailView, ProductPriceCreateView, ProductPriceUpdateView, ProductPriceDeleteView,
    cart_list_view, import_cart_view, CartDetailView, CartCreateView, CartUpdateView, CartDeleteView,
     CartProductsDetailView, CartProductsCreateView, CartProductsUpdateView, CartProductsDeleteView,
)


urlpatterns = [
    path('', home_view, name='home'),  # Page d'accueil
    path('inpc/', inpc_view, name='calculer-inpc'), 
    path('communes/', commune_list_view, name='commune-list'),
    path('communes/import/', import_data_view, name='import_data'),
    # Point of Sale URLs
    path('points-of-sale/', point_of_sale_list_view, name='pointofsale-list'),
    path("points-of-sale/import/", import_point_of_sale_view, name="pointofsale-import"),
    path('point-of-sale/create/', PointOfSaleCreateView.as_view(), name='pointofsale-create'),
    path('point-of-sale/<int:pk>/', PointOfSaleDetailView.as_view(), name='pointofsale-detail'),
    path('point-of-sale/<int:pk>/update/', PointOfSaleUpdateView.as_view(), name='pointofsale-update'),
    path('point-of-sale/<int:pk>/delete/', PointOfSaleDeleteView.as_view(), name='pointofsale-delete'),

    # Product URLs
    path('product/', product_list_view, name='product-list'),
    path("product/import/", import_product_view, name="product-import"),
    path('product/create/', ProductCreateView.as_view(), name='product-create'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),

    # Product Price URLs
    path('product-price/', productprice_list_view, name='productprice-list'),
    path("product-price/import/", import_productprice_view, name="productprice-import"),
    path('product-price/create/', ProductPriceCreateView.as_view(), name='productprice-create'),
    path('product-price/<int:pk>/', ProductPriceDetailView.as_view(), name='productprice-detail'),
    path('product-price/<int:pk>/update/', ProductPriceUpdateView.as_view(), name='productprice-update'),
    path('product-price/<int:pk>/delete/', ProductPriceDeleteView.as_view(), name='productprice-delete'),

    # Cart URLs
    path('cart/', cart_list_view, name='cart-list'),
    path('cart/import/', import_cart_view, name='cart-import'),
    path('cart/create/', CartCreateView.as_view(), name='cart-create'),
    path('cart/<int:pk>/', CartDetailView.as_view(), name='cart-detail'),
    path('cart/<int:pk>/update/', CartUpdateView.as_view(), name='cart-update'),
    path('cart/<int:pk>/delete/', CartDeleteView.as_view(), name='cart-delete'),

    # Cart Products URLs
    path('cart-products/', cartproducts_list_view, name='cartproducts-list'),
    path('cart-products/import/', import_cartproducts_view, name='cartproducts-import'),
    path('cart-products/create/', CartProductsCreateView.as_view(), name='cartproducts-create'),
    path('cart-products/<int:pk>/', CartProductsDetailView.as_view(), name='cartproducts-detail'),
    path('cart-products/<int:pk>/update/', CartProductsUpdateView.as_view(), name='cartproducts-update'),
    path('cart-products/<int:pk>/delete/', CartProductsDeleteView.as_view(), name='cartproducts-delete'),
]
