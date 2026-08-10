from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, Department

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['role'] = user.role
        token['username'] = user.username
        
        # Add employee specific claims if employee profile exists
        if hasattr(user, 'employee_profile'):
            token['employee_id'] = user.employee_profile.id
            if user.employee_profile.department:
                token['department'] = user.employee_profile.department.name

        return token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']
        read_only_fields = ['id']

class DepartmentSerializer(serializers.ModelSerializer):
    manager_name = serializers.CharField(source='manager.get_full_name', read_only=True)

    class Meta:
        model = Department
        fields = ['id', 'name', 'manager', 'manager_name', 'budget', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
