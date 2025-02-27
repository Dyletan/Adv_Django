# trading/tests.py
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from trading.models import Order, Transaction
from trading.serializers import OrderSerializer, TransactionSerializer
from products.models import Product, Category
from users.models import CustomUser

class TradingTests(APITestCase): # Renamed class for brevity

    def setUp(self):
        self.seller = CustomUser.objects.create_user(username='seller_trade_test', password='password', role='trader')
        self.buyer = CustomUser.objects.create_user(username='buyer_trade_test', password='password', role='customer')
        self.category = Category.objects.create(name='Trading Test Category')
        self.product = Product.objects.create(name='Trade Product', price=100.00, seller=self.seller, category=self.category)

    def test_create_order_authenticated(self):
        self.client.force_authenticate(user=self.buyer) # Buyer places order
        url = reverse('order-create')
        data = {
            'product': self.product.pk,
            'order_type': 'buy',
            'quantity': 2,
            'price': 100.00
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.get()
        self.assertEqual(order.user, self.buyer) # Verify order user is buyer
        self.assertEqual(order.product, self.product)

    def test_create_order_unauthenticated(self):
        url = reverse('order-create')
        data = {
            'product': self.product.pk,
            'order_type': 'buy',
            'quantity': 2,
            'price': 100.00
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_order_list_authenticated(self):
        order1 = Order.objects.create(user=self.buyer, product=self.product, order_type='buy', quantity=1, price=99.00)
        order2 = Order.objects.create(user=self.buyer, product=self.product, order_type='sell', quantity=3, price=101.00)
        self.client.force_authenticate(user=self.buyer)
        url = reverse('order-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        orders = Order.objects.filter(user=self.buyer)
        serializer = OrderSerializer(orders, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_get_order_list_unauthenticated(self):
        url = reverse('order-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_order_detail_authenticated_own_order(self):
        order = Order.objects.create(user=self.buyer, product=self.product, order_type='buy', quantity=2, price=100.00)
        self.client.force_authenticate(user=self.buyer)
        url = reverse('order-detail', args=[order.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = OrderSerializer(order)
        self.assertEqual(response.data, serializer.data)

    def test_get_order_detail_authenticated_other_user_order(self): # Simulate another user trying to access
        other_user = CustomUser.objects.create_user(username='other_user', password='password')
        order = Order.objects.create(user=other_user, product=self.product, order_type='buy', quantity=2, price=100.00)
        self.client.force_authenticate(user=self.buyer) # Buyer tries to access other user's order
        url = reverse('order-detail', args=[order.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) # Or 403 Forbidden, depending on desired security

    def test_get_order_detail_unauthenticated(self):
        order = Order.objects.create(user=self.buyer, product=self.product, order_type='buy', quantity=2, price=100.00)
        url = reverse('order-detail', args=[order.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Transaction list is just an example - you can add more specific transaction tests if needed.
    def test_get_transaction_list_authenticated(self):
         # Create some orders and transactions for testing if needed
         self.client.force_authenticate(user=self.buyer)
         url = reverse('transaction-list')
         response = self.client.get(url)
         self.assertEqual(response.status_code, status.HTTP_200_OK) # Might be empty list if no transactions