from django.contrib import admin

from .models import Certification, EducationRecord, Employee, EmployeeSkill, EmploymentHistory, PromotionHistory


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "phone", "employment_type", "status", "date_joined")
    list_filter = ("status",)
    search_fields = ("first_name", "last_name")


admin.site.register([EmploymentHistory, EducationRecord, Certification, EmployeeSkill, PromotionHistory])
