from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """
    Custom user model. Every logged-in person in NuruX — regardless of
    whether they end up with a full Employee record — authenticates through
    this model. `role` drives RBAC enforcement at the API layer (PRD §8).
    """

    class Role(models.TextChoices):
        SUPER_ADMIN = "super_admin", "Super Admin"
        HR_OFFICER = "hr_officer", "HR Officer"
        MANAGER = "manager", "Manager"
        PAYROLL_OFFICER = "payroll_officer", "Payroll/Finance Officer"
        DIRECTOR = "director", "Director/Executive"
        EMPLOYEE = "employee", "Employee"
        APPLICANT = "applicant", "Applicant"
        RECEPTIONIST = "receptionist", "Receptionist"

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=32, choices=Role.choices, default=Role.EMPLOYEE)

    # --- Account lockout tracking (PRD §9 — Security) ---
    failed_login_attempts = models.PositiveSmallIntegerField(default=0)
    locked_until = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    @property
    def is_locked(self) -> bool:
        return bool(self.locked_until and self.locked_until > timezone.now())

    def register_failed_login(self):
        from django.conf import settings

        self.failed_login_attempts += 1
        if self.failed_login_attempts >= settings.MAX_FAILED_LOGIN_ATTEMPTS:
            self.locked_until = timezone.now() + timezone.timedelta(
                minutes=settings.LOCKOUT_DURATION_MINUTES
            )
        self.save(update_fields=["failed_login_attempts", "locked_until"])

    def register_successful_login(self):
        self.failed_login_attempts = 0
        self.locked_until = None
        self.save(update_fields=["failed_login_attempts", "locked_until"])
