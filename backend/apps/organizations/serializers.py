from rest_framework import serializers

from .models import Department, Role


class DepartmentSerializer(serializers.ModelSerializer):
    manager_name = serializers.SerializerMethodField(read_only=True)
    parent_department_name = serializers.CharField(
        source="parent_department.name", read_only=True, default=None
    )

    class Meta:
        model = Department
        fields = [
            "id",
            "name",
            "manager",
            "manager_name",
            "budget",
            "parent_department",
            "parent_department_name",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_manager_name(self, obj):
        return str(obj.manager) if obj.manager else None

    def validate_parent_department(self, value):
        # Prevent a department from being its own ancestor.
        instance = getattr(self, "instance", None)
        if instance and value and value.pk == instance.pk:
            raise serializers.ValidationError("A department cannot be its own parent.")
        return value


class RoleSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source="department.name", read_only=True, default=None)

    class Meta:
        model = Role
        fields = [
            "id",
            "title",
            "salary_grade",
            "department",
            "department_name",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
