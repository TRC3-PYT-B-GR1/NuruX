from rest_framework import filters, viewsets
from rest_framework.permissions import BasePermission

from .models import AuditLog
from .serializers import AuditLogSerializer


class IsSuperAdmin(BasePermission):
    """
    Audit logs are deliberately restricted to Super Admin, not the broader
    FULL_WRITE_ROLES (Super Admin + HR Officer) used elsewhere — this is
    the record of who-did-what across the whole platform, including HR's
    own actions, so HR itself shouldn't be able to browse or (implicitly)
    infer gaps in its own audit trail.
    """

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and (user.is_superuser or user.role == "super_admin"))


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    GET /api/v1/audit/logs/            list (filterable)
    GET /api/v1/audit/logs/{id}/       detail

    No create/update/delete exposed — entries are written server-side only,
    via apps.audit.services.log_action(), never through this API.

    Query params:
      ?search=employee.exited
      ?action=employee.exited
      ?target_type=employees.Employee
      ?actor=<user_id>
      ?ordering=-timestamp
    """

    queryset = AuditLog.objects.select_related("actor").all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsSuperAdmin]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["action", "target_type", "target_repr"]
    ordering_fields = ["timestamp", "action"]

    def get_queryset(self):
        queryset = super().get_queryset()
        action_param = self.request.query_params.get("action")
        target_type = self.request.query_params.get("target_type")
        actor_id = self.request.query_params.get("actor")
        if action_param:
            queryset = queryset.filter(action=action_param)
        if target_type:
            queryset = queryset.filter(target_type=target_type)
        if actor_id:
            queryset = queryset.filter(actor_id=actor_id)
        return queryset
