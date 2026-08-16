# from django.conf import settings
# from django.db import models


# class Employee(models.Model):
#     """
#     Phase-1 stub. This exists now only so that:
#       - every User can (optionally) be linked to a person record, and
#       - Department/Role FKs added in later phases have somewhere to point.

#     Full fields (personal details, employment history, next of kin,
#     salary grade, etc. — PRD §7.1) are added in Phase 3 (Employee CRUD).
#     Deliberately no `department`/`role` FK yet — those models don't exist
#     until Phase 2, and adding them now would just mean a migration rewrite.
#     """

#     class Status(models.TextChoices):
#         ACTIVE = "active", "Active"
#         SUSPENDED = "suspended", "Suspended"
#         EXITED = "exited", "Exited"

#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name="employee_profile",
#     )
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     status = models.CharField(max_length=16, choices=Status.choices, default=Status.ACTIVE)
#     date_joined = models.DateField(null=True, blank=True)
#     department = models.ForeignKey(
#         "organizations.Department",
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name="employees",
#     )
#     role = models.ForeignKey(
#         "organizations.Role",
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name="employees",
#     )
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ["last_name", "first_name"]

#     def __str__(self):
#         return f"{self.first_name} {self.last_name} ({self.get_status_display()})"

from django.conf import settings
from django.db import models


class Employee(models.Model):
    """
    Employee/person record for the NuruX HRMS.
    Links 1:1 with the User model for authentication.
    """

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        SUSPENDED = "suspended", "Suspended"
        EXITED = "exited", "Exited"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="employee_profile",
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    date_joined = models.DateField(
        null=True,
        blank=True,
    )

    department = models.ForeignKey(
        "organizations.Department",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="employees",
    )

    role = models.ForeignKey(
        "organizations.Role",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="employees",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.get_status_display()})"