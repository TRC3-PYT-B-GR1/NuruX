from rest_framework import serializers

from .models import CertificationType, EmployeeCertification, EmployeeSkill, Skill


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "name", "category", "created_at"]
        read_only_fields = ["id", "created_at"]


class CertificationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CertificationType
        fields = ["id", "name", "issuing_body", "category", "created_at"]
        read_only_fields = ["id", "created_at"]


class EmployeeSkillSerializer(serializers.ModelSerializer):
    """
    `employee` is deliberately read-only: it's set server-side from the URL
    (/employees/{employee_id}/skills/) in the view, never taken from the
    request body — otherwise a client could add a skill entry to someone
    else's record just by changing a field value.
    """

    skill_name = serializers.CharField(source="skill.name", read_only=True)

    class Meta:
        model = EmployeeSkill
        fields = ["id", "employee", "skill", "skill_name", "proficiency", "created_at"]
        read_only_fields = ["id", "employee", "created_at"]


class EmployeeCertificationSerializer(serializers.ModelSerializer):
    certification_type_name = serializers.CharField(source="certification_type.name", read_only=True)

    class Meta:
        model = EmployeeCertification
        fields = [
            "id",
            "employee",
            "certification_type",
            "certification_type_name",
            "issue_date",
            "expiry_date",
            "certificate_file",
            "created_at",
        ]
        read_only_fields = ["id", "employee", "created_at"]

    def validate(self, attrs):
        issue_date = attrs.get("issue_date", getattr(self.instance, "issue_date", None))
        expiry_date = attrs.get("expiry_date", getattr(self.instance, "expiry_date", None))
        if issue_date and expiry_date and expiry_date < issue_date:
            raise serializers.ValidationError({"expiry_date": "Expiry date cannot be before the issue date."})
        return attrs
