from django.conf import settings
from django.db import models
from django.utils import timezone


class Employee(models.Model):
    """
    Single source of truth for the employee record (PRD §7.1 — Employee
    Management). Built up in phases:
      Phase 1: `user` link + name + status stub
      Phase 2: `department` / `role` FKs, once those catalogs existed
      Phase 3 (here): full personal/employment details, `manager` self-FK,
                       next-of-kin & emergency contact, soft-delete lifecycle

    Employees are NOT hard-deleted from this system (downstream attendance/
    leave/payroll history must stay intact) — `status` moves to EXITED
    instead. See EmployeeViewSet.destroy().
    """

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        SUSPENDED = "suspended", "Suspended"
        EXITED = "exited", "Exited"

    class Gender(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"
        OTHER = "other", "Other"
        UNDISCLOSED = "undisclosed", "Prefer not to say"

    class EmploymentType(models.TextChoices):
        FULL_TIME = "full_time", "Full-time"
        PART_TIME = "part_time", "Part-time"
        CONTRACT = "contract", "Contract"
        INTERN = "intern", "Intern"

    # --- Identity / account link ---
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="employee_profile",
    )

    # --- Personal details ---
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=16, choices=Gender.choices, default=Gender.UNDISCLOSED)
    date_of_birth = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True, help_text="Work/contact email — distinct from login username.")
    phone_number = models.CharField(max_length=30, blank=True)
    residential_address = models.TextField(blank=True)
    national_id_number = models.CharField(max_length=50, blank=True, null=True, unique=True)

    # --- Employment ---
    employment_type = models.CharField(
        max_length=16, choices=EmploymentType.choices, default=EmploymentType.FULL_TIME
    )
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.ACTIVE)
    date_joined = models.DateField(null=True, blank=True)
    exit_date = models.DateField(null=True, blank=True)
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
    manager = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="direct_reports",
        help_text="This employee's direct supervisor (drives the Manager 'own team' scope in RBAC).",
    )

    # --- Next of kin / emergency contact ---
    next_of_kin_name = models.CharField(max_length=150, blank=True)
    next_of_kin_relationship = models.CharField(max_length=100, blank=True)
    next_of_kin_phone = models.CharField(max_length=30, blank=True)
    emergency_contact_name = models.CharField(max_length=150, blank=True)
    emergency_contact_phone = models.CharField(max_length=30, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.get_status_display()})"

    def mark_exited(self):
        self.status = self.Status.EXITED
        self.exit_date = timezone.now().date()
        self.save(update_fields=["status", "exit_date", "updated_at"])

    def reactivate(self):
        self.status = self.Status.ACTIVE
        self.exit_date = None
        self.save(update_fields=["status", "exit_date", "updated_at"])
