from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ("username", "email", "role", "is_active", "is_locked", "last_login")
    list_filter = ("role", "is_active", "is_staff")
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("NuruX", {"fields": ("role", "failed_login_attempts", "locked_until")}),
    )

    @admin.display(boolean=True, description="Locked")
    def is_locked(self, obj):
        return obj.is_locked
