from django.contrib import admin

from .models import CertificationType, EmployeeCertification, EmployeeSkill, Skill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    search_fields = ("name", "category")


@admin.register(CertificationType)
class CertificationTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "issuing_body", "category")
    search_fields = ("name", "issuing_body", "category")


@admin.register(EmployeeSkill)
class EmployeeSkillAdmin(admin.ModelAdmin):
    list_display = ("employee", "skill", "proficiency", "created_at")
    list_filter = ("proficiency", "skill")
    search_fields = ("employee__first_name", "employee__last_name", "skill__name")
    autocomplete_fields = ("employee", "skill")


@admin.register(EmployeeCertification)
class EmployeeCertificationAdmin(admin.ModelAdmin):
    list_display = ("employee", "certification_type", "issue_date", "expiry_date")
    list_filter = ("certification_type",)
    search_fields = ("employee__first_name", "employee__last_name", "certification_type__name")
    autocomplete_fields = ("employee", "certification_type")
