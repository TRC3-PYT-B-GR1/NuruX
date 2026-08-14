from django.contrib import admin

from .models import Department, Role


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "manager", "parent_department", "budget")
    search_fields = ("name",)
    list_filter = ("parent_department",)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("title", "department", "salary_grade")
    search_fields = ("title",)
    list_filter = ("department",)
