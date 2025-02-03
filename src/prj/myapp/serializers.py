# myapp/serializers.py
from rest_framework import serializers
from .models import Commune, Wilaya, PointOfSale, Product, ProductPrice, Moughataa
import json


# Serializer for Moughataa
class MoughataaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moughataa
        fields = ('id', 'name', 'code', 'wilaya')

# myapp/serializers.py
from rest_framework import serializers
from .models import Commune, Wilaya, PointOfSale
import json

class WilayaGeoJSONSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    geometry = serializers.SerializerMethodField()
    properties = serializers.SerializerMethodField()

    class Meta:
        model = Wilaya
        fields = ('type', 'geometry', 'properties')

    def get_type(self, obj):
        return "Feature"

    def get_geometry(self, obj):
        if obj.polygon:
            try:
                return json.loads(obj.polygon)
            except json.JSONDecodeError:
                return None
        return None

    def get_properties(self, obj):
        return {
            'id': obj.id,
            'name': obj.name,
            'code': obj.code,
            # Explicitly check for None so that 0 is preserved.
            'inpc': float(obj.inpc) if obj.inpc is not None else None
        }

class MoughataaGeoJSONSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    geometry = serializers.SerializerMethodField()
    properties = serializers.SerializerMethodField()

    class Meta:
        model = Moughataa
        fields = ('type', 'geometry', 'properties')

    def get_type(self, obj):
        return "Feature"

    def get_geometry(self, obj):
        if obj.polygon:
            import json
            return json.loads(obj.polygon)
        return None

    def get_properties(self, obj):
        return {
            'id': obj.id,
            'name': obj.name,
            'code': obj.code,
            'wilaya': obj.wilaya.code if obj.wilaya else None,
            'inpc': str(obj.inpc) if obj.inpc is not None else None,
        }
    
class CommuneGeoJSONSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    geometry = serializers.SerializerMethodField()
    properties = serializers.SerializerMethodField()

    class Meta:
        model = Commune
        fields = ('type', 'geometry', 'properties')

    def get_type(self, obj):
        return "Feature"

    def get_geometry(self, obj):
        if obj.polygon:
            try:
                return json.loads(obj.polygon)
            except json.JSONDecodeError:
                return None
        return None

    def get_properties(self, obj):
        return {
            'id': obj.id,
            'name': obj.name,
            'code': obj.code,
            'inpc': float(obj.inpc) if obj.inpc is not None else None
        }


# Serializer for PointOfSale
class PointOfSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointOfSale
        fields = ('id', 'code', 'type', 'gps_lat', 'gps_lon', 'commune')

# Serializer for Product
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'code', 'name', 'description', 'unit_measure', 'product_type')

# Serializer for ProductPrice
class ProductPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPrice
        fields = ('id', 'value', 'date_from', 'date_to', 'product', 'point_of_sale')