from django.contrib import admin
from .models import ProductType, Product, Wilaya, Moughataa, Commune, PointOfSale, ProductPrice, Cart, CartProducts

# Customize the admin for the Product model
class ProductAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'product_type', 'unit_measure')  # Fields to display in the list view
    list_filter = ('product_type',)  # Add filters for the 'product_type' field
    search_fields = ('code', 'name')  # Enable search by code and name

# Register your models here.
admin.site.register(ProductType)
admin.site.register(Product, ProductAdmin) # Register Product with the custom admin
admin.site.register(Wilaya)
admin.site.register(Moughataa)
admin.site.register(Commune)
admin.site.register(PointOfSale)
admin.site.register(ProductPrice)
admin.site.register(Cart)
admin.site.register(CartProducts)