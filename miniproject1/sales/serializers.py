from rest_framework import serializers
from .models import SalesOrder, SalesOrderItem, Invoice
from products.models import Product
from users.models import User

class SalesOrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name') # Display product name
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product')

    class Meta:
        model = SalesOrderItem
        fields = '__all__'

class SalesOrderSerializer(serializers.ModelSerializer):
    sales_representative_username = serializers.ReadOnlyField(source='sales_representative.username') # Display username
    sales_representative_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='sales_representative'), source='sales_representative') # For setting sales rep by ID
    customer_username = serializers.ReadOnlyField(source='customer.username')
    customer_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='customer'), source='customer')
    items = SalesOrderItemSerializer(many=True, read_only=True) # Nested serializer for items
    item_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False) # For creating/updating items, accepting list of item IDs

    class Meta:
        model = SalesOrder
        fields = '__all__'

    def create(self, validated_data):
        item_ids = validated_data.pop('item_ids', []) # Extract item IDs
        sales_order = SalesOrder.objects.create(**validated_data) # Create sales order first
        for item_data in item_ids: # Assuming you're passing a list of item data dictionaries
             SalesOrderItem.objects.create(sales_order=sales_order, **item_data) # Create sales order items
        return sales_order


class InvoiceSerializer(serializers.ModelSerializer):
    sales_order_details = SalesOrderSerializer(source='sales_order', read_only=True) # Nested for sales order details

    class Meta:
        model = Invoice
        fields = '__all__'