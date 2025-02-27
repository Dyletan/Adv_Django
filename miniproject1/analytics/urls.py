from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnalyticsReportViewSet

router = DefaultRouter()
router.register(r'reports', AnalyticsReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
]