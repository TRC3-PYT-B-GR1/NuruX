from django.db.models import Q
from rest_framework.permissions import SAFE_METHODS, BasePermission

ADMIN_ROLES = {"super_admin"}
HR_ROLES = {"hr_officer"}
FULL_WRITE_ROLES = ADMIN_ROLES | HR_ROLES
READ_ONLY_ORG_WIDE_ROLES = {"director", "payroll_officer"}


def get_visible_employees(user):
    """
    The single source of truth for "which Employee rows can this user see",
    per PRD §8. Built for EmployeeViewSet.get_queryset() in Phase 3; reused
    as-is by apps.skills' employee-linked endpoints in Phase 4 so the two
    modules can't silently drift out of sync on who's allowed to see whom.
    """
    from apps.employees.models import Employee  # local import avoids app-loading order issues

    base = Employee.objects.all()

    if not (user and user.is_authenticated):
        return base.none()

    if user.is_superuser or user.role in FULL_WRITE_ROLES or user.role in READ_ONLY_ORG_WIDE_ROLES:
        return base

    if user.role == "manager":
        employee_profile = getattr(user, "employee_profile", None)
        if not employee_profile:
            return base.none()
        return base.filter(
            Q(manager_id=employee_profile.id)
            | Q(department__manager_id=employee_profile.id)
            | Q(id=employee_profile.id)
        )

    if user.role == "employee":
        employee_profile = getattr(user, "employee_profile", None)
        return base.filter(id=employee_profile.id) if employee_profile else base.none()

    return base.none()


class EmployeePermission(BasePermission):
    """
    Implements the Employee-Records column of PRD §8's permissions matrix:

        Super Admin / HR Officer : Full
        Director                : View-only, org-wide
        Payroll/Finance Officer  : View relevant fields  (*)
        Manager                  : View own team (read-only)
        Employee                 : View/edit own record only

    (*) Field-level restriction for Payroll Officer is not yet implemented —
    they currently get the same read access as Director. Tightening this to
    "relevant fields only" needs a dedicated serializer and is deferred to
    the permissions/audit hardening pass, once Payroll data exists to reason
    about. Flagged here deliberately rather than silently skipped.

    Row-level scoping (a Manager only seeing their own team, an Employee
    only seeing themselves) happens in EmployeeViewSet.get_queryset() and
    is reinforced here at the object level as a second line of defense.
    """

    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated):
            return False

        if view.action == "create":
            return user.is_superuser or user.role in FULL_WRITE_ROLES

        if view.action == "destroy":
            return user.is_superuser or user.role in FULL_WRITE_ROLES

        if view.action in ("reactivate",):
            return user.is_superuser or user.role in FULL_WRITE_ROLES

        # list / retrieve / update / partial_update / me — allowed through
        # to object-level and queryset-level checks below.
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_superuser or user.role in FULL_WRITE_ROLES:
            return True

        is_self = bool(obj.user_id and obj.user_id == user.id)

        if user.role in READ_ONLY_ORG_WIDE_ROLES:
            return request.method in SAFE_METHODS

        if user.role == "manager":
            manages_directly = obj.manager_id and getattr(user, "employee_profile", None) and obj.manager_id == user.employee_profile.id
            heads_department = (
                obj.department_id
                and getattr(user, "employee_profile", None)
                and obj.department
                and obj.department.manager_id == user.employee_profile.id
            )
            if request.method in SAFE_METHODS:
                return bool(manages_directly or heads_department or is_self)
            return is_self  # a manager can edit their own record, not their reports'

        if user.role == "employee":
            return is_self

        return False
