from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        SUPER_ADMIN = 'SUPER_ADMIN', 'Super Admin'
        HR_OFFICER = 'HR_OFFICER', 'HR Officer'
        MANAGER = 'MANAGER', 'Manager'
        PAYROLL_OFFICER = 'PAYROLL_OFFICER', 'Payroll/Finance Officer'
        EMPLOYEE = 'EMPLOYEE', 'Employee'
        DIRECTOR = 'DIRECTOR', 'Director/Executive'
        APPLICANT = 'APPLICANT', 'Applicant'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.EMPLOYEE,
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_departments',
        help_text="The manager responsible for this department."
    )
    budget = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
        help_text="Allocated budget for the department."
    )
    description = models.TextField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, help_text="Expected office latitude")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, help_text="Expected office longitude")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
