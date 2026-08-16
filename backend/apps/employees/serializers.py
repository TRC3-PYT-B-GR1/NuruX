from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from apps.organizations.models import Department, Role
from apps.organizations.serializers import DepartmentSerializer, RoleSerializer
from .models import Employee

User = get_user_model()

class EmployeeSerializer(serializers.ModelSerializer):
    department_details = DepartmentSerializer(source='department', read_only=True)
    role_details = RoleSerializer(source='role', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    rbac_role = serializers.CharField(source='user.role', read_only=True)

    class Meta:
        model = Employee
        fields = [
            'id', 'first_name', 'last_name', 'status', 'date_joined',
            'department', 'role', 'department_details', 'role_details', 'email',
            'rbac_role', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        if instance.user:
            instance.user.first_name = instance.first_name
            instance.user.last_name = instance.last_name
            instance.user.save(update_fields=['first_name', 'last_name'])
        return instance

    def validate(self, attrs):
        department = attrs.get('department', getattr(self.instance, 'department', None))
        role = attrs.get('role', getattr(self.instance, 'role', None))
        if role and role.department_id and role.department_id != getattr(department, 'id', None):
            raise serializers.ValidationError(
                {'role': 'The selected role belongs to a different department.'}
            )
        return attrs


class EmployeeCreateSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8, trim_whitespace=False)
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())
    rbac_role = serializers.ChoiceField(choices=User.Role.choices, default=User.Role.EMPLOYEE)

    def validate_email(self, value):
        value = value.strip().lower()
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError('A user with this email already exists.')
        return value

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate(self, attrs):
        role = attrs['role']
        department = attrs['department']
        if role.department_id and role.department_id != department.id:
            raise serializers.ValidationError(
                {'role': 'The selected role belongs to a different department.'}
            )
        return attrs
