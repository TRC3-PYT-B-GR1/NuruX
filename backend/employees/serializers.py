from rest_framework import serializers
from .models import Employee
from core.serializers import UserSerializer, DepartmentSerializer

class EmployeeSerializer(serializers.ModelSerializer):
    # Depending on the view, we might want nested representations
    # For now, we return basic info and user details
    user_details = UserSerializer(source='user', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = Employee
        fields = [
            'id', 'user', 'user_details', 'department', 'department_name', 
            'role_title', 'salary_grade', 'employment_type', 'status',
            'phone_number', 'address', 'date_of_birth', 'hire_date',
            'next_of_kin', 'emergency_contact', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
