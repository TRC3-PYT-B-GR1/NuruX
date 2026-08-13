from django.contrib import admin

from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "actor", "action", "target_type", "target_repr")
    list_filter = ("action", "target_type")
    search_fields = ("actor__username", "action", "target_repr")
    readonly_fields = [f.name for f in AuditLog._meta.fields]  # entirely read-only in admin too

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
