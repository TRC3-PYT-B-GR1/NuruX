from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.common.permissions import IsAdminOrHR
from .models import EmployeeAsset, AssetAssignment, AssetReturn, MaintenanceHistory
from .serializers import EmployeeAssetSerializer, AssetAssignmentSerializer, AssetReturnSerializer, MaintenaceHistorySerializer


class EmployeeAssetListCreateAPIView(generics.ListCreateAPIView):
    queryset = EmployeeAsset.objects.all()
    serializer_class = EmployeeAssetSerializer
    permission_classes = [IsAuthenticated, IsAdminOrHR]
    
class AssetAssignmentListCreateAPIView(generics.ListCreateAPIView):
    queryset = AssetAssignment.objects.all()
    serializer_class = AssetAssignmentSerializer
    permission_classes = [IsAuthenticated, IsAdminOrHR]
    
class AssetReturnListCreateAPIView(generics.ListCreateAPIView):
    queryset = AssetReturn.objects.all()
    serializer_class = AssetReturnSerializer
    permission_classes = [IsAuthenticated, IsAdminOrHR]
    
class MaintenanceHistoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = MaintenanceHistory.objects.all()
    serializer_class = MaintenaceHistorySerializer
    permission_classes = [IsAuthenticated, IsAdminOrHR]

# Create your views here.
