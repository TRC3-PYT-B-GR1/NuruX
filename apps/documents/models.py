from django.conf import settings
from django.db import models


class EmployeeDocument(models.Model):
    """
    Employment paperwork: offer letters, contracts, promotion/warning
    letters, certificates, signed documents (PRD §7.2).

    Versioning: deliberately lightweight — no separate DocumentVersion
    table. Uploading a new document of the same (employee, document_type)
    supersedes the previous one: the old record's `is_current` flips to
    False and stays queryable via `supersedes` for history, rather than
    being overwritten or deleted. See EmployeeDocumentListCreateView.perform_create().

    Never hard-deleted: DELETE archives (`is_archived=True`) rather than
    removing the row — these are legal/audit-relevant records.
    """

    class DocumentType(models.TextChoices):
        OFFER_LETTER = "offer_letter", "Offer Letter"
        CONTRACT = "contract", "Contract"
        PROMOTION_LETTER = "promotion_letter", "Promotion Letter"
        WARNING_LETTER = "warning_letter", "Warning Letter"
        CERTIFICATE = "certificate", "Certificate"
        SIGNED_DOCUMENT = "signed_document", "Signed Document"
        OTHER = "other", "Other"

    class Sensitivity(models.TextChoices):
        PUBLIC = "public", "Public"
        INTERNAL = "internal", "Internal"
        CONFIDENTIAL = "confidential", "Confidential"

    employee = models.ForeignKey(
        "employees.Employee", on_delete=models.CASCADE, related_name="documents"
    )
    document_type = models.CharField(max_length=32, choices=DocumentType.choices)
    title = models.CharField(max_length=200, blank=True)
    file = models.FileField(upload_to="employee_documents/%Y/%m/")
    sensitivity = models.CharField(
        max_length=16, choices=Sensitivity.choices, default=Sensitivity.INTERNAL
    )

    version_number = models.PositiveIntegerField(default=1)
    supersedes = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True, related_name="superseded_by"
    )
    is_current = models.BooleanField(default=True)

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="uploaded_documents",
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_archived = models.BooleanField(default=False)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"{self.employee} — {self.get_document_type_display()} v{self.version_number}"
