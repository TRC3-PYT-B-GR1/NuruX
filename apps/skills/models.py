from django.db import models


class Skill(models.Model):
    """
    Catalog of skills an employee can hold. Kept as its own lookup table
    (rather than free text on Employee) so reporting/filtering ("who knows
    Python?") is possible later without string-matching. The join to
    Employee (with proficiency level) is built in the Employee CRUD phase.
    """

    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class CertificationType(models.Model):
    """
    Catalog of certification types (e.g. "PMP", "CIPM", "ACCA") — distinct
    from the record of *who holds it and when it expires*, which is the
    EmployeeCertification join model built in the Employee CRUD phase.
    """

    name = models.CharField(max_length=150, unique=True)
    issuing_body = models.CharField(max_length=150, blank=True)
    category = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class EmployeeSkill(models.Model):
    """
    Join: which employees hold which skills, at what level. Self-declared —
    an employee can add/remove their own (see apps.skills.permissions) —
    HR/Admin can manage anyone's.
    """

    class Proficiency(models.TextChoices):
        BEGINNER = "beginner", "Beginner"
        INTERMEDIATE = "intermediate", "Intermediate"
        ADVANCED = "advanced", "Advanced"
        EXPERT = "expert", "Expert"

    employee = models.ForeignKey(
        "employees.Employee", on_delete=models.CASCADE, related_name="employee_skills"
    )
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name="employee_links")
    proficiency = models.CharField(
        max_length=16, choices=Proficiency.choices, default=Proficiency.INTERMEDIATE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["skill__name"]
        unique_together = ("employee", "skill")  # one entry per skill per employee — re-adding updates proficiency instead

    def __str__(self):
        return f"{self.employee} — {self.skill} ({self.get_proficiency_display()})"


class EmployeeCertification(models.Model):
    """
    Join: which employees hold which certifications, with supporting proof.

    Deliberately NOT unique_together(employee, certification_type) — an
    employee can legitimately re-certify (e.g. PMP renewal) and we want the
    history, not just the latest record. If you only want the current one
    shown, filter by expiry_date in the view/serializer rather than
    constraining it at the DB level.
    """

    employee = models.ForeignKey(
        "employees.Employee", on_delete=models.CASCADE, related_name="certifications"
    )
    certification_type = models.ForeignKey(
        CertificationType, on_delete=models.CASCADE, related_name="employee_links"
    )
    issue_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    certificate_file = models.FileField(upload_to="certifications/%Y/%m/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-issue_date"]

    def __str__(self):
        return f"{self.employee} — {self.certification_type}"
