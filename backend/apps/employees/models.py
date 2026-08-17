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
    phone = models.CharField(max_length=30, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=30, blank=True)
    nationality = models.CharField(max_length=80, blank=True)
    identification_number = models.CharField(max_length=100, blank=True)

    class EmploymentType(models.TextChoices):
        FULL_TIME = "full_time", "Full time"
        PART_TIME = "part_time", "Part time"
        CONTRACT = "contract", "Contract"
        TEMPORARY = "temporary", "Temporary"
        INTERN = "intern", "Intern"

    employment_type = models.CharField(max_length=20, choices=EmploymentType.choices, default=EmploymentType.FULL_TIME)
    salary_grade = models.CharField(max_length=50, blank=True)

    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    date_joined = models.DateField(
        null=True,
        blank=True,
    )

    manager = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="direct_reports",
    )
    exit_date = models.DateField(null=True, blank=True)
    exit_reason = models.TextField(blank=True)

    next_of_kin_name = models.CharField(max_length=160, blank=True)
    next_of_kin_relationship = models.CharField(max_length=80, blank=True)
    next_of_kin_phone = models.CharField(max_length=30, blank=True)
    next_of_kin_address = models.TextField(blank=True)
    emergency_contact_name = models.CharField(max_length=160, blank=True)
    emergency_contact_relationship = models.CharField(max_length=80, blank=True)
    emergency_contact_phone = models.CharField(max_length=30, blank=True)
    emergency_contact_address = models.TextField(blank=True)

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


class EmploymentHistory(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="employment_history")
    employer = models.CharField(max_length=200)
    job_title = models.CharField(max_length=160)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-start_date", "-id"]


class EducationRecord(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="education_records")
    institution = models.CharField(max_length=200)
    qualification = models.CharField(max_length=160)
    field_of_study = models.CharField(max_length=160, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-end_date", "-id"]


class Certification(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="certifications")
    name = models.CharField(max_length=180)
    issuer = models.CharField(max_length=180, blank=True)
    issue_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    credential_id = models.CharField(max_length=120, blank=True)

    class Meta:
        ordering = ["-issue_date", "-id"]


class EmployeeSkill(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="skills")
    name = models.CharField(max_length=120)
    proficiency = models.CharField(max_length=30, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["employee", "name"], name="unique_employee_skill")]
        ordering = ["name"]


class PromotionHistory(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="promotion_history")
    previous_role = models.CharField(max_length=160, blank=True)
    new_role = models.CharField(max_length=160)
    effective_date = models.DateField()
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-effective_date", "-id"]
