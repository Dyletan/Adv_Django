# products/tests.py
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from products.models import Category, Product
from products.serializers import CategorySerializer, ProductSerializer
from users.models import CustomUser # Import CustomUser for creating seller

class ProductTests(APITestCase): # Renamed class for brevity

    def setUp(self):
        self.category1 = Category.objects.create(name='Electronics', description='Test Category')
        self.seller = CustomUser.objects.create_user(username='seller_test', password='password', role='trader')

    def test_category_list(self):
        url = reverse('category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_category_detail(self):
        url = reverse('category-detail', args=[self.category1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = CategorySerializer(self.category1)
        self.assertEqual(response.data, serializer.data)

    def test_product_list(self):
        Product.objects.create(name='Test Product', price=100.00, seller=self.seller, category=self.category1)
        url = reverse('product-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_create_product_authenticated(self):
        self.client.force_authenticate(user=self.seller)
        url = reverse('product-list-create')
        data = {
            'name': 'New Product',
            'description': 'Product Description',
            'quantity': 5,
            'price': 50.00,
            'category': self.category1.pk # Send category PK
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().name, 'New Product')
        self.assertEqual(Product.objects.get().seller, self.seller) # Verify seller is correctly set

    def test_create_product_unauthenticated(self):
        url = reverse('product-list-create')
        data = {
            'name': 'New Product',
            'description': 'Product Description',
            'quantity': 5,
            'price': 50.00,
            'category': self.category1.pk
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_product_detail(self):
        product = Product.objects.create(name='Detail Product', price=150.00, seller=self.seller, category=self.category1)
        url = reverse('product-detail-update-delete', args=[product.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = ProductSerializer(product)
        self.assertEqual(response.data, serializer.data)

    def test_update_product_authenticated(self):
        product = Product.objects.create(name='Initial Product', price=200.00, seller=self.seller, category=self.category1)
        self.client.force_authenticate(user=self.seller)
        url = reverse('product-detail-update-delete', args=[product.pk])
        updated_data = {
            'name': 'Updated Product',
            'description': 'Updated Description',
            'quantity': 10,
            'price': 250.00,
            'category': self.category1.pk
        }
        response = self.client.put(url, updated_data) # or patch
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.get(pk=product.pk).name, 'Updated Product')

    def test_update_product_unauthenticated(self):
        product = Product.objects.create(name='Initial Product', price=200.00, seller=self.seller, category=self.category1)
        url = reverse('product-detail-update-delete', args=[product.pk])
        updated_data = {'name': 'Updated Product'}
        response = self.client.put(url, updated_data) # or patch
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_product_authenticated(self):
        product = Product.objects.create(name='Product to Delete', price=300.00, seller=self.seller, category=self.category1)
        self.client.force_authenticate(user=self.seller)
        url = reverse('product-detail-update-delete', args=[product.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)

    def test_delete_product_unauthenticated(self):
        product = Product.objects.create(name='Product to Delete', price=300.00, seller=self.seller, category=self.category1)
        url = reverse('product-detail-update-delete', args=[product.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)