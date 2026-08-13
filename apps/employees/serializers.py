from rest_framework import serializers

from .models import Employee


class EmployeeListSerializer(serializers.ModelSerializer):
    """Lightweight — used for GET /employees/ so large org listings stay cheap."""

    full_name = serializers.SerializerMethodField()
    department_name = serializers.CharField(source="department.name", read_only=True, default=None)
    role_title = serializers.CharField(source="role.title", read_only=True, default=None)

    class Meta:
        model = Employee
        fields = [
            "id",
            "full_name",
            "email",
            "department",
            "department_name",
            "role",
            "role_title",
            "status",
            "employment_type",
            "date_joined",
        ]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class EmployeeDetailSerializer(serializers.ModelSerializer):
    """Full record — GET/POST/PATCH on a single employee. HR/Admin use only (see permissions.py)."""

    department_name = serializers.CharField(source="department.name", read_only=True, default=None)
    role_title = serializers.CharField(source="role.title", read_only=True, default=None)
    manager_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Employee
        fields = [
            "id",
            "user",
            "first_name",
            "middle_name",
            "last_name",
            "gender",
            "date_of_birth",
            "email",
            "phone_number",
            "residential_address",
            "national_id_number",
            "employment_type",
            "status",
            "date_joined",
            "exit_date",
            "department",
            "department_name",
            "role",
            "role_title",
            "manager",
            "manager_name",
            "next_of_kin_name",
            "next_of_kin_relationship",
            "next_of_kin_phone",
            "emergency_contact_name",
            "emergency_contact_phone",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "status", "exit_date", "created_at", "updated_at"]
        # `status`/`exit_date` are deliberately read-only here — they change
        # only through the dedicated exit/reactivate actions, so there's one
        # code path that enforces the status-lifecycle rules, not two.

    def get_manager_name(self, obj):
        return str(obj.manager) if obj.manager else None

    def validate(self, attrs):
        role = attrs.get("role", getattr(self.instance, "role", None))
        department = attrs.get("department", getattr(self.instance, "department", None))
        if role and department and role.department_id and role.department_id != department.id:
            raise serializers.ValidationError(
                {"role": "This role belongs to a different department than the one selected."}
            )
        return attrs

    def validate_manager(self, value):
        if value and self.instance and value.pk == self.instance.pk:
            raise serializers.ValidationError("An employee cannot be their own manager.")
        return value


class EmployeePayrollSerializer(serializers.ModelSerializer):
    """
    PRD §8: Payroll/Finance Officer gets "view relevant fields" on Employee
    Records — not the full detail record. This is that restriction, closed
    out in Phase 6 (flagged as deferred back in Phase 3's permissions.py).

    "Relevant" here = identity + employment structure needed to run payroll
    (department, role → salary grade, employment type, status, join date).
    Deliberately excludes: DOB, address, national ID, next-of-kin, and
    emergency contact — none of that is payroll's business.
    """

    full_name = serializers.SerializerMethodField()
    department_name = serializers.CharField(source="department.name", read_only=True, default=None)
    role_title = serializers.CharField(source="role.title", read_only=True, default=None)
    salary_grade = serializers.CharField(source="role.salary_grade", read_only=True, default=None)

    class Meta:
        model = Employee
        fields = [
            "id",
            "full_name",
            "email",
            "department",
            "department_name",
            "role",
            "role_title",
            "salary_grade",
            "employment_type",
            "status",
            "date_joined",
        ]
        read_only_fields = fields  # Payroll Officer gets read-only access here regardless

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class EmployeeSelfServiceSerializer(serializers.ModelSerializer):
    """
    What an Employee can edit on their OWN record (PRD §5 — Employee persona:
    "Self-service for leave, payslips, profile"). Deliberately excludes
    department/role/manager/status/employment_type — those are HR-managed.
    """

    class Meta:
        model = Employee
        fields = [
            "id",
            "first_name",
            "middle_name",
            "last_name",
            "phone_number",
            "residential_address",
            "next_of_kin_name",
            "next_of_kin_relationship",
            "next_of_kin_phone",
            "emergency_contact_name",
            "emergency_contact_phone",
        ]
        read_only_fields = ["id"]
