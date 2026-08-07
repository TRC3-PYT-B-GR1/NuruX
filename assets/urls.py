from django.urls import path
from .views import (
    EmployeeAssetListCreateAPIView,
    AssetAssignmentListCreateAPIView,
    AssetReturnListCreateAPIView,
    MaintenanceHistoryListCreateAPIView
)


urlpatterns = [
    path('assets/', EmployeeAssetListCreateAPIView.as_view(), name='assets-list'),
    path('assignments/', AssetAssignmentListCreateAPIView.as_view(), name='assignments-list'),
    path('return/', AssetReturnListCreateAPIView.as_view(), name='return-list'),
    path('history/', MaintenanceHistoryListCreateAPIView.as_view(), name='history-list'),
]