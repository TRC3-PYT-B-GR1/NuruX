from rest_framework import serializers
from .models import EmployeeAsset, AssetAssignment, AssetReturn, MaintenanceHistory


class EmployeeAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeAsset
        fields = '__all__'
        
class AssetAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetAssignment
        fields = '__all__'
        
class AssetReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetReturn
        fields = '__all__'
        
        
class MaintenaceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceHistory
        fields = '__all__'