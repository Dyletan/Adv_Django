from django.contrib import admin
from django.urls import path, include
from .views import index_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('products.urls')),
    path('api/', include('trading.urls')),
    path('api/', include('sales.urls')),
    path('api/', include('analytics.urls')),
    path('api/', include('notifications.urls')),
    path('', index_view, name='index'),
    path('', include('products.urls')),
    path('', include('trading.urls')),
    path('', include('sales.urls')),
    path('', include('users.urls')),
]