from rest_framework.permissions import SAFE_METHODS, BasePermission

from apps.employees.permissions import FULL_WRITE_ROLES


class EmployeeLinkedResourcePermission(BasePermission):
    """
    Applies to EmployeeSkill / EmployeeCertification objects.

    Read: governed entirely by queryset scoping in the view (which reuses
    apps.employees.permissions.get_visible_employees) — if you can see the
    employee, you can see their skills/certifications.

    Write (create/update/delete): Admin/HR can manage anyone's; an employee
    can manage only their own (self-declared skills/certs). Manager/
    Director/Payroll get read-only here, same as they do on the Employee
    record itself.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_superuser or user.role in FULL_WRITE_ROLES:
            return True
        if request.method in SAFE_METHODS:
            return True  # queryset already restricted visibility before we got here
        return bool(obj.employee.user_id and obj.employee.user_id == user.id)
