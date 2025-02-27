from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from users.models import CustomUser

class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        category_id = self.request.query_params.get('category')
        queryset = Product.objects.all()
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

class AddProductView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role not in ["admin", "trader", "sales_rep"]:
            return Response({"error": "You do not have permission to create a product."}, status=status.HTTP_403_FORBIDDEN)

        serializer = ProductSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(seller=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CategoryListView(generics.ListAPIView):
    """Список всех категорий"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class AddCategoryView(generics.CreateAPIView):
    """Создание новой категории"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]