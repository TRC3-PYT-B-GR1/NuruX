from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.audit.services import log_action

from .permissions import FULL_WRITE_ROLES, EmployeePermission, get_visible_employees
from .serializers import (
    EmployeeDetailSerializer,
    EmployeeListSerializer,
    EmployeePayrollSerializer,
    EmployeeSelfServiceSerializer,
)


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    /api/v1/employees/                GET, POST
    /api/v1/employees/{id}/           GET, PATCH, DELETE (soft)
    /api/v1/employees/{id}/reactivate/   POST  (admin/HR)
    /api/v1/employees/me/                GET, PATCH  (self-service)

    Query params on list:
      ?search=jane            (first/last name, email)
      ?department=<id>
      ?role=<id>
      ?status=active|suspended|exited
      ?ordering=last_name / -date_joined
    """

    permission_classes = [EmployeePermission]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["first_name", "last_name", "email", "phone_number"]
    ordering_fields = ["last_name", "date_joined", "status", "created_at"]

    def get_queryset(self):
        """
        Row-level RBAC (PRD §8). This is the primary enforcement point —
        EmployeePermission.has_object_permission is the second line of
        defense for single-object requests, but list results are governed
        entirely by what queryset we hand back here.

        Scoping logic itself lives in permissions.get_visible_employees()
        so apps.skills' employee-linked endpoints (Phase 4) see exactly the
        same "who can see whom" rules without duplicating them.
        """
        queryset = get_visible_employees(self.request.user).select_related("department", "role", "manager")

        department_id = self.request.query_params.get("department")
        role_id = self.request.query_params.get("role")
        status_param = self.request.query_params.get("status")
        if department_id:
            queryset = queryset.filter(department_id=department_id)
        if role_id:
            queryset = queryset.filter(role_id=role_id)
        if status_param:
            queryset = queryset.filter(status=status_param)

        return queryset

    def get_serializer_class(self):
        user = self.request.user
        if user.is_authenticated and user.role == "payroll_officer" and not user.is_superuser:
            # PRD §8: "view relevant fields" only — closes the gap flagged
            # in Phase 3. Applies to list/retrieve; Payroll can't write
            # Employee records at all (EmployeePermission denies it), so
            # there's no create/update path to worry about restricting.
            return EmployeePayrollSerializer
        if self.action == "list":
            return EmployeeListSerializer
        if self.action == "me":
            return EmployeeSelfServiceSerializer
        if self.action in ("update", "partial_update"):
            if not (user.is_superuser or user.role in FULL_WRITE_ROLES):
                # A Manager/Employee editing their own record via
                # /employees/{id}/ (rather than /employees/me/) still only
                # gets the restricted field set — EmployeePermission already
                # ensures they can only reach this path for their own object.
                return EmployeeSelfServiceSerializer
        return EmployeeDetailSerializer

    def destroy(self, request, *args, **kwargs):
        """
        Soft delete: an employee record is never hard-deleted (it's the
        anchor for attendance/leave/payroll history in later phases).
        DELETE instead moves status -> exited.
        """
        employee = self.get_object()
        previous_status = employee.status
        employee.mark_exited()
        log_action(
            actor=request.user,
            action="employee.exited",
            target=employee,
            changes={"status": {"from": previous_status, "to": employee.status}},
            request=request,
        )
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"])
    def reactivate(self, request, pk=None):
        """POST /employees/{id}/reactivate/ — admin/HR only (see EmployeePermission)."""
        employee = self.get_object()
        previous_status = employee.status
        employee.reactivate()
        log_action(
            actor=request.user,
            action="employee.reactivated",
            target=employee,
            changes={"status": {"from": previous_status, "to": employee.status}},
            request=request,
        )
        return Response(EmployeeDetailSerializer(employee).data)

    @action(detail=False, methods=["get", "patch"])
    def me(self, request):
        """Self-service: an authenticated user's own employee record."""
        employee_profile = getattr(request.user, "employee_profile", None)
        if not employee_profile:
            return Response(
                {"detail": "No employee record is linked to this account."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if request.method == "GET":
            return Response(EmployeeDetailSerializer(employee_profile).data)

        serializer = EmployeeSelfServiceSerializer(employee_profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
