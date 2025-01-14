from django.db import models


# Product Type Model
class ProductType(models.Model):
    code = models.CharField(max_length=45, unique=True)
    label = models.CharField(max_length=45)
    description = models.CharField(max_length=45)

    def __str__(self):
        return self.label

# Product Model
class Product(models.Model):
    code = models.CharField(max_length=45, unique=True)
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=45)
    unit_measure = models.CharField(max_length=45)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# Wilaya Model
class Wilaya(models.Model):
    code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=252)

    def __str__(self):
        return self.name


# Moughataa Model
class Moughataa(models.Model):
    code = models.CharField(max_length=45, unique=True)
    label = models.CharField(max_length=45)
    wilaya = models.ForeignKey(Wilaya, on_delete=models.CASCADE)

    def __str__(self):
        return self.label


# Commune Model
class Commune(models.Model):
    code = models.CharField(max_length=45, unique=True)
    name = models.CharField(max_length=45)
    moughataa = models.ForeignKey(Moughataa, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# Point of Sale Model
class PointOfSale(models.Model):
    code = models.CharField(max_length=45, unique=True)
    type = models.CharField(max_length=45)
    gps_lat = models.FloatField()
    gps_lon = models.FloatField()
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE)

    def __str__(self):
        return self.code


# Product Price Model
class ProductPrice(models.Model):
    value = models.FloatField()
    date_from = models.DateField()
    date_to = models.DateField(null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    point_of_sale = models.ForeignKey(PointOfSale, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} - {self.value}"


# Cart Model
class Cart(models.Model):
    code = models.CharField(max_length=45, unique=True)
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=45)

    def __str__(self):
        return self.name


class CartProducts(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)  # Renommé en 'cart'
    weight = models.FloatField()
    date_from = models.DateField()
    date_to = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.cart.name} - {self.product.name}"

