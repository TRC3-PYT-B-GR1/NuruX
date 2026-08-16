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
            "description",
            "manager",
            "manager_name",
            "budget",
            "parent_department",
            "parent_department_name",
            "latitude",
            "longitude",
            "geofence_radius_meters",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_manager_name(self, obj):
        return str(obj.manager) if obj.manager else None

    def validate_parent_department(self, value):
        instance = getattr(self, "instance", None)
        ancestor = value
        while instance and ancestor:
            if ancestor.pk == instance.pk:
                raise serializers.ValidationError("A department hierarchy cannot contain a cycle.")
            ancestor = ancestor.parent_department
        return value

    def validate(self, attrs):
        latitude = attrs.get("latitude", getattr(self.instance, "latitude", None))
        longitude = attrs.get("longitude", getattr(self.instance, "longitude", None))
        if (latitude is None) != (longitude is None):
            raise serializers.ValidationError(
                "Latitude and longitude must either both be provided or both be empty."
            )
        return attrs


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
