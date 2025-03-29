from rest_framework import serializers
from .models import Manufacturer, Product


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = "__all__"  # Include all fields


class ProductSerializer(serializers.ModelSerializer):
    manufacturer_name = serializers.ReadOnlyField(
        source="manufacturer.name"
    )  # Display manufacturer name

    class Meta:
        model = Product
        fields = "__all__"
