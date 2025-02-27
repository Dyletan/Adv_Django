from rest_framework import serializers
from .models import Product, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True) # To display category details in product API
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category') # For setting category by ID on product creation/update

    class Meta:
        model = Product
        fields = '__all__'