from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrHR(BasePermission):
    """
    Full access (read + write) restricted to Super Admin and HR Officer.

    Per PRD §8's permissions matrix, Department/Role/Skill/Certification
    catalogs are HR/Admin-managed data — enforced here at the API layer,
    not left to the frontend to hide buttons for (§8: "a manager's JWT
    should be structurally incapable of pulling another department's
    payroll data, not just prevented by the interface").
    """

    allowed_roles = {"super_admin", "hr_officer"}

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and (user.is_superuser or user.role in self.allowed_roles)
        )


class IsAdminOrHRWriteElseReadOnly(BasePermission):
    """
    Read access to any authenticated user, write access restricted to
    Super Admin / HR Officer. Useful later for catalogs that other roles
    (e.g. Manager, Employee) need to browse but not edit — not used by
    Phase 2's ViewSets yet, kept here for the next phase.
    """

    allowed_roles = {"super_admin", "hr_officer"}

    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated):
            return False
        if request.method in SAFE_METHODS:
            return True
        return user.is_superuser or user.role in self.allowed_roles


class IsExecutive(BasePermission):
    """Allow only platform administrators and directors/executives."""

    allowed_roles = {"super_admin", "director"}

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and (user.is_superuser or user.role in self.allowed_roles)
        )


class IsPayrollAdminOrReadOnlyExecutive(BasePermission):
    """Payroll staff administer payroll; directors may only read reports."""

    payroll_roles = {"super_admin", "payroll_officer"}
    read_roles = payroll_roles | {"director"}

    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated):
            return False
        if user.is_superuser:
            return True
        if request.method in SAFE_METHODS:
            return user.role in self.read_roles
        return user.role in self.payroll_roles


class IsManagerOrHR(BasePermission):
    """Allow staff who are authorized to manage people records."""

    allowed_roles = {"super_admin", "hr_officer", "manager", "director"}

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and (user.is_superuser or user.role in self.allowed_roles)
        )
