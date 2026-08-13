from django.contrib import admin

from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "department",
        "role",
        "manager",
        "status",
        "employment_type",
        "date_joined",
    )
    list_filter = ("status", "employment_type", "department", "gender")
    search_fields = ("first_name", "last_name", "email", "phone_number", "national_id_number")
    autocomplete_fields = ("department", "role", "manager", "user")
