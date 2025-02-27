from rest_framework import viewsets
from .models import AnalyticsReport
from .serializers import AnalyticsReportSerializer
from .permissions import CanViewAnalyticsReport

class AnalyticsReportViewSet(viewsets.ReadOnlyModelViewSet): # Analytics reports are read-only
    queryset = AnalyticsReport.objects.all().order_by('-generated_at')
    serializer_class = AnalyticsReportSerializer
    permission_classes = [CanViewAnalyticsReport] # Admin and Traders can view reports