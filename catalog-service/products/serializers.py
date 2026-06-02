from decimal import Decimal, ROUND_HALF_UP

from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2, write_only=True)
    price_display = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'price_cents', 'price_display', 'stock', 'category', 'created_at', 'updated_at']
        read_only_fields = ['id', 'price_cents', 'price_display', 'created_at', 'updated_at']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('Le prix doit être strictement positif.')
        if value > Decimal('99999999.99'):
            raise serializers.ValidationError('Le prix ne peut pas dépasser 99 999 999,99 €.')
        return value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    def validate_stock(self, value):
        if value > 100000:
            raise serializers.ValidationError('Le stock ne peut pas dépasser 100 000 unités.')
        return value

    def get_price_display(self, obj):
        return Decimal(obj.price_cents) / Decimal('100')

    def create(self, validated_data):
        price = validated_data.pop('price')
        validated_data['price_cents'] = self._to_cents(price)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        price = validated_data.pop('price', None)
        if price is not None:
            validated_data['price_cents'] = self._to_cents(price)
        return super().update(instance, validated_data)

    def _to_cents(self, price):
        return int((price * 100).quantize(Decimal('1'), rounding=ROUND_HALF_UP))
