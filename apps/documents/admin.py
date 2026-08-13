from django.contrib import admin

from .models import EmployeeDocument


@admin.register(EmployeeDocument)
class EmployeeDocumentAdmin(admin.ModelAdmin):
    list_display = (
        "employee",
        "document_type",
        "sensitivity",
        "version_number",
        "is_current",
        "is_archived",
        "uploaded_by",
        "uploaded_at",
    )
    list_filter = ("document_type", "sensitivity", "is_current", "is_archived")
    search_fields = ("employee__first_name", "employee__last_name", "title")
    autocomplete_fields = ("employee", "uploaded_by", "supersedes")