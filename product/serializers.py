from rest_framework import serializers
from .models import Product, Category, Review

class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(source='products.count', read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'products_count']

        def validate_name(self, value):
            if not value.strip():
                raise serializers.ValidationError('Название категории не может быть пустым.')
            if len(value) < 2:
                raise serializers.ValidationError('Название категории должно содержать минимум 2 символа.')
            return value

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category']

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError('Название продукта не может быть пустым.')
        return value

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError('Цена не может быть отрицательной.')
        return value

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError('Название продукта не может быть пустым.')
        return value

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError('Цена не может быть отрицательной.')
        return value

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'text', 'product', 'stars']

    def validate_text(self, value):
        if not value.strip():
            raise serializers.ValidationError('Текст отзыва не может быть пустым.')
        return value

    def validate_stars(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError('Оценка должна быть от 1 до 5.')
        return value