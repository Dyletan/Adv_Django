from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet, product_list_view, product_detail_view

router = DefaultRouter()
router.register(r'api/products', ProductViewSet) # API product views under /api/
router.register(r'api/categories', CategoryViewSet) # API category views under /api/

urlpatterns = [
    path('api/', include(router.urls)), # API urls are prefixed with /api/
    path('products-html/', product_list_view, name='product-list-html'), # HTML product list
    path('products-html/<int:pk>/', product_detail_view, name='product-detail-html'), # HTML product detail
]