from django.contrib import admin
from .models import Product, ProductPrice, Cart, CartProducts, Wilaya, Moughataa, Commune, PointOfSale

# Register your models here
admin.site.register(Product)
admin.site.register(ProductPrice)
admin.site.register(Cart)
admin.site.register(CartProducts)
admin.site.register(Wilaya)
admin.site.register(Moughataa)
admin.site.register(Commune)
admin.site.register(PointOfSale)
