# myapp/models.py

from django.db import models

class ProductType(models.Model):
    code = models.CharField(max_length=45, unique=True)
    label = models.CharField(max_length=45)
    description = models.CharField(max_length=45)

    def __str__(self):
        return self.label

class Product(models.Model):
    code = models.CharField(max_length=45, unique=True)
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=45)
    unit_measure = models.CharField(max_length=45)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Wilaya(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Moughataa(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    code = models.CharField(max_length=50, unique=True)
    wilaya = models.ForeignKey(Wilaya, on_delete=models.CASCADE, related_name="moughataas")

    def __str__(self):
        return self.name

class Commune(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    moughataa = models.ForeignKey(Moughataa, on_delete=models.CASCADE, related_name="communes")

    def __str__(self):
        return self.name

class PointOfSale(models.Model):
    code = models.CharField(max_length=45, unique=True)
    type = models.CharField(max_length=45)
    gps_lat = models.FloatField()  # Si ces champs ne sont pas utilisés dans les calculs financiers, FloatField est acceptable
    gps_lon = models.FloatField()
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE)

    def __str__(self):
        return self.code

class ProductPrice(models.Model):
    value = models.DecimalField(max_digits=10, decimal_places=2)  # Utilisez DecimalField
    date_from = models.DateField()
    date_to = models.DateField(null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    point_of_sale = models.ForeignKey(PointOfSale, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} - {self.value}"

class Cart(models.Model):
    code = models.CharField(max_length=45, unique=True)
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=45)

    def __str__(self):
        return self.name

class CartProducts(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cartproducts')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=5, decimal_places=2)  # Utilisez DecimalField
    date_from = models.DateField()
    date_to = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.cart.name} - {self.product.name}"
