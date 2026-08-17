from django.contrib import admin

from .models import Candidate, JobPosting


@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ("title", "department", "status", "date_posted")
    list_filter = ("status", "department")
    search_fields = ("title", "department")


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ("full_name", "job", "stage", "score", "applied_at")
    list_filter = ("stage", "job")
    search_fields = ("full_name", "email")
