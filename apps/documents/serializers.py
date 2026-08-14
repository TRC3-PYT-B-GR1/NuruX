from rest_framework import serializers

from .models import EmployeeDocument


class EmployeeDocumentSerializer(serializers.ModelSerializer):
    """
    `employee`, `version_number`, `supersedes`, `is_current`, `uploaded_by`
    are all read-only: they're computed/assigned server-side in the view
    (versioning logic + auditability), never taken from the request body.
    """

    uploaded_by_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = EmployeeDocument
        fields = [
            "id",
            "employee",
            "document_type",
            "title",
            "file",
            "sensitivity",
            "version_number",
            "supersedes",
            "is_current",
            "uploaded_by",
            "uploaded_by_name",
            "uploaded_at",
        ]
        read_only_fields = [
            "id",
            "employee",
            "version_number",
            "supersedes",
            "is_current",
            "uploaded_by",
            "uploaded_at",
        ]

    def get_uploaded_by_name(self, obj):
        return obj.uploaded_by.username if obj.uploaded_by else None
