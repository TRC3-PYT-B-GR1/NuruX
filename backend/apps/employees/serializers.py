from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from apps.organizations.models import Department, Role
from apps.organizations.serializers import DepartmentSerializer, RoleSerializer
from .models import Certification, EducationRecord, Employee, EmployeeSkill, EmploymentHistory, PromotionHistory

User = get_user_model()

class EmploymentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EmploymentHistory
        exclude = ["employee"]


class EducationRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationRecord
        exclude = ["employee"]


class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        exclude = ["employee"]


class EmployeeSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeSkill
        exclude = ["employee"]


class PromotionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionHistory
        exclude = ["employee"]


class EmploymentHistoryApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmploymentHistory
        fields = "__all__"


class EducationRecordApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationRecord
        fields = "__all__"


class CertificationApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = "__all__"


class EmployeeSkillApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeSkill
        fields = "__all__"


class PromotionHistoryApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionHistory
        fields = "__all__"


class EmployeeSerializer(serializers.ModelSerializer):
    department_details = DepartmentSerializer(source='department', read_only=True)
    role_details = RoleSerializer(source='role', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    rbac_role = serializers.CharField(source='user.role', read_only=True)
    manager_name = serializers.SerializerMethodField(read_only=True)
    employment_history = EmploymentHistorySerializer(many=True, read_only=True)
    education_records = EducationRecordSerializer(many=True, read_only=True)
    certifications = CertificationSerializer(many=True, read_only=True)
    skills = EmployeeSkillSerializer(many=True, read_only=True)
    promotion_history = PromotionHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Employee
        fields = [
            'id', 'first_name', 'last_name', 'phone', 'address', 'date_of_birth',
            'gender', 'nationality', 'identification_number', 'employment_type',
            'salary_grade', 'status', 'date_joined', 'manager', 'manager_name',
            'exit_date', 'exit_reason', 'next_of_kin_name', 'next_of_kin_relationship',
            'next_of_kin_phone', 'next_of_kin_address', 'emergency_contact_name',
            'emergency_contact_relationship', 'emergency_contact_phone',
            'emergency_contact_address',
            'department', 'role', 'department_details', 'role_details', 'email',
            'rbac_role', 'employment_history', 'education_records', 'certifications',
            'skills', 'promotion_history', 'created_at', 'updated_at'
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

    def get_manager_name(self, obj):
        return f'{obj.manager.first_name} {obj.manager.last_name}'.strip() if obj.manager else None


class EmployeeCreateSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8, trim_whitespace=False)
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())
    rbac_role = serializers.ChoiceField(choices=User.Role.choices, default=User.Role.EMPLOYEE)
    phone = serializers.CharField(max_length=30, required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    date_of_birth = serializers.DateField(required=False, allow_null=True)
    gender = serializers.CharField(max_length=30, required=False, allow_blank=True)
    nationality = serializers.CharField(max_length=80, required=False, allow_blank=True)
    identification_number = serializers.CharField(max_length=100, required=False, allow_blank=True)
    employment_type = serializers.ChoiceField(choices=Employee.EmploymentType.choices, required=False)
    salary_grade = serializers.CharField(max_length=50, required=False, allow_blank=True)
    manager = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), required=False, allow_null=True)
    emergency_contact_name = serializers.CharField(max_length=160, required=False, allow_blank=True)
    emergency_contact_relationship = serializers.CharField(max_length=80, required=False, allow_blank=True)
    emergency_contact_phone = serializers.CharField(max_length=30, required=False, allow_blank=True)
    emergency_contact_address = serializers.CharField(required=False, allow_blank=True)
    next_of_kin_name = serializers.CharField(max_length=160, required=False, allow_blank=True)
    next_of_kin_relationship = serializers.CharField(max_length=80, required=False, allow_blank=True)
    next_of_kin_phone = serializers.CharField(max_length=30, required=False, allow_blank=True)
    next_of_kin_address = serializers.CharField(required=False, allow_blank=True)

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
