from django.conf import settings
from django.db import models
from django.core.validators import FileExtensionValidator


class JobPosting(models.Model):
    class Status(models.TextChoices):
        OPEN = "open", "Open"
        CLOSED = "closed", "Closed"

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    department = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.OPEN)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="job_postings")
    date_posted = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_posted"]

    def __str__(self):
        return self.title


class Candidate(models.Model):
    class Stage(models.TextChoices):
        APPLIED = "applied", "Applied"
        SCREENING = "screening", "Screening"
        INTERVIEW = "interview", "Interview"
        OFFER = "offer", "Offer"
        REJECTED = "rejected", "Rejected"
        HIRED = "hired", "Hired"

    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name="candidates")
    full_name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    stage = models.CharField(max_length=20, choices=Stage.choices, default=Stage.APPLIED)
    score = models.PositiveSmallIntegerField(default=0)
    resume = models.FileField(
        upload_to="recruitment/resumes/",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=["pdf", "doc", "docx"])],
    )
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-applied_at"]

    def __str__(self):
        return f"{self.full_name} - {self.job.title}"
