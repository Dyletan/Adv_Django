from django.urls import path
from products.views import *

urlpatterns = [
    path('', ProductListView.as_view(), name='api_product_list'),
    path('add/', AddProductView.as_view(), name='api_add_product'),
    path('<int:product_id>/', ProductDetailView.as_view(), name='api_product_detail'),
    
    path('categories/', CategoryListView.as_view(), name='api_category_list'),
    path('categories/add/', AddCategoryView.as_view(), name='api_add_category'),
]