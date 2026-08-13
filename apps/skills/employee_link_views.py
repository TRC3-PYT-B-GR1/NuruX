from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from apps.employees.permissions import FULL_WRITE_ROLES, get_visible_employees

from .models import EmployeeCertification, EmployeeSkill
from .permissions import EmployeeLinkedResourcePermission
from .serializers import EmployeeCertificationSerializer, EmployeeSkillSerializer


class _EmployeeScopedMixin:
    """
    Shared plumbing for both sub-resources: resolve the parent Employee from
    the URL, but only if the requesting user is allowed to see that Employee
    at all (reuses the exact same visibility rule as EmployeeViewSet).
    """

    def get_employee(self):
        employee_id = self.kwargs["employee_id"]
        visible = get_visible_employees(self.request.user)
        return get_object_or_404(visible, pk=employee_id)

    def check_write_access(self, employee):
        user = self.request.user
        is_self = bool(employee.user_id and employee.user_id == user.id)
        if not (user.is_superuser or user.role in FULL_WRITE_ROLES or is_self):
            raise PermissionDenied(
                "You do not have permission to add records for this employee."
            )


class EmployeeSkillListCreateView(_EmployeeScopedMixin, generics.ListCreateAPIView):
    """
    GET  /api/v1/employees/{employee_id}/skills/
    POST /api/v1/employees/{employee_id}/skills/
    """

    serializer_class = EmployeeSkillSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        employee = self.get_employee()
        return EmployeeSkill.objects.filter(employee=employee).select_related("skill")

    def perform_create(self, serializer):
        employee = self.get_employee()
        self.check_write_access(employee)
        serializer.save(employee=employee)


class EmployeeSkillDetailView(_EmployeeScopedMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    GET/PATCH/DELETE /api/v1/employees/{employee_id}/skills/{id}/
    """

    serializer_class = EmployeeSkillSerializer
    permission_classes = [IsAuthenticated, EmployeeLinkedResourcePermission]

    def get_queryset(self):
        employee = self.get_employee()
        return EmployeeSkill.objects.filter(employee=employee).select_related("skill")


class EmployeeCertificationListCreateView(_EmployeeScopedMixin, generics.ListCreateAPIView):
    """
    GET  /api/v1/employees/{employee_id}/certifications/
    POST /api/v1/employees/{employee_id}/certifications/   (multipart for certificate_file)
    """

    serializer_class = EmployeeCertificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        employee = self.get_employee()
        return EmployeeCertification.objects.filter(employee=employee).select_related("certification_type")

    def perform_create(self, serializer):
        employee = self.get_employee()
        self.check_write_access(employee)
        serializer.save(employee=employee)


class EmployeeCertificationDetailView(_EmployeeScopedMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    GET/PATCH/DELETE /api/v1/employees/{employee_id}/certifications/{id}/
    """

    serializer_class = EmployeeCertificationSerializer
    permission_classes = [IsAuthenticated, EmployeeLinkedResourcePermission]

    def get_queryset(self):
        employee = self.get_employee()
        return EmployeeCertification.objects.filter(employee=employee).select_related("certification_type")
