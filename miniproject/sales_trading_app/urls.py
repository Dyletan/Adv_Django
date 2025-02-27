from django.contrib import admin
from django.urls import path, include
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('products/', include('products.urls')),
    path('trading/', include('trading.urls')),
    path('sales/', include('sales.urls'))
]

schema_view = get_schema_view(
    openapi.Info(
        title="Trading API",
        default_version='v1',
        description="API documentation for Trading and Sales system",
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns += [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]