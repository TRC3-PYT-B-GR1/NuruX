from django.shortcuts import render
from rest_framework import generics
from .models import EmployeeAsset, AssetAssignment, AssetReturn, MaintenanceHistory
from .serializers import EmployeeAssetSerializer, AssetAssignmentSerializer, AssetReturnSerializer, MaintenaceHistorySerializer


class EmployeeAssetListCreateAPIView(generics.ListCreateAPIView):
    queryset = EmployeeAsset.objects.all()
    serializer_class = EmployeeAssetSerializer
    
class AssetAssignmentListCreateAPIView(generics.ListCreateAPIView):
    queryset = AssetAssignment.objects.all()
    serializer_class = AssetAssignmentSerializer
    
class AssetReturnListCreateAPIView(generics.ListCreateAPIView):
    queryset = AssetReturn.objects.all()
    serializer_class = AssetReturnSerializer
    
class MaintenanceHistoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = MaintenanceHistory.objects.all()
    serializer_class = MaintenaceHistorySerializer

# Create your views here.
