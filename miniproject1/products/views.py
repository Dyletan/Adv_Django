from rest_framework import viewsets
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from .permissions import CanManageProduct, CanManageCategory, CanViewProduct
from django.shortcuts import render, get_object_or_404

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [CanManageCategory] # Only Admin can manage categories

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [CanViewProduct] # Everyone with product view permission can list/retrieve categories
        else: # create, update, partial_update, destroy
            permission_classes = [CanManageCategory] # Only admin can modify categories
        return [permission() for permission in permission_classes]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('name')
    serializer_class = ProductSerializer

    def get_permissions(self):
        """
        - list, retrieve: Trader, SalesRep, Customer, Admin can view
        - create, update, partial_update, destroy: Trader, Admin can manage
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [CanViewProduct] # Traders, SalesReps, Customers, Admins can view
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [CanManageProduct] # Admins and Traders can manage products
        else: # Default - restrict to those who can manage products
            permission_classes = [CanManageProduct]
        return [permission() for permission in permission_classes]

def product_list_view(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})