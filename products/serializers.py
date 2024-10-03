from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("El campo Nombre es obligatorio.")
        return value

    def validate_description(self, value):
        if not value:
            raise serializers.ValidationError("El campo Descripción es obligatorio.")
        return value
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("El campo Precio debe ser un número mayor que 0.")
        return value

    def validate_stock(self, value):
        if value <= 0:
            raise serializers.ValidationError("El campo Stock debe ser un número mayor que 0.")
        return value
