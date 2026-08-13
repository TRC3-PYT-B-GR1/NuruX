from django.db import models


class Department(models.Model):
    """
    The org chart that everything else (approvals, attendance, payroll)
    hangs off of — PRD §7.1. Supports MDA-style or branch-style hierarchies
    via parent_department.
    """

    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True, null=True)

    manager = models.ForeignKey(
        "employees.Employee",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="departments_managed",
        help_text="Employee who heads this department.",
    )

    budget = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        null=True,
        blank=True,
    )

    parent_department = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sub_departments",
    )
    
    # Geo-fencing coordinates
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Role(models.Model):
    """Job role/title, tied to a salary grade and usually a department."""

    title = models.CharField(max_length=150)

    salary_grade = models.CharField(
        max_length=50,
        blank=True,
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="roles",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]
        unique_together = ("title", "department")

    def __str__(self):
        return (
            f"{self.title} ({self.department.name})"
            if self.department
            else self.title
        )