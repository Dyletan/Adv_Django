from rest_framework import serializers
from .models import Order, Transaction
from products.models import Product

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username') # Display username, not user ID
    product_name = serializers.ReadOnlyField(source='product.name') # Display product name
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product') # Allow setting product by ID

    class Meta:
        model = Order
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    buy_order_details = OrderSerializer(source='buy_order', read_only=True) # Nested serializer for details
    sell_order_details = OrderSerializer(source='sell_order', read_only=True)

    class Meta:
        model = Transaction
        fields = '__all__'