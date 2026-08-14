from django.conf import settings
from django.db import models


class AuditLog(models.Model):
    """
    "Every payroll change, leave approval, and permission change is
    attributable to a user, timestamped, and immutable in the audit log"
    (PRD §9 — Auditability). Payroll/leave don't exist yet in this build,
    but the same principle applies to what we do have: employee status
    changes, document archival, and user role/lockout events.

    `action` is a free-text slug (e.g. "employee.exited") rather than a
    fixed choices field — new sensitive actions get added over time as
    later phases (payroll, leave) ship, and a hardcoded enum would need a
    migration every time. Trade-off: no DB-level validation of the value:
    calls should go through log_action() in services.py, which is the
    single place that constructs these strings, rather than writing
    AuditLog.objects.create(...) ad hoc around the codebase.
    """

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="audit_logs",
        help_text="Who performed the action. Null if the actor account was later deleted.",
    )
    action = models.CharField(max_length=100, help_text='e.g. "employee.exited", "user.role_changed"')
    target_type = models.CharField(max_length=100, help_text='e.g. "employees.Employee"')
    target_id = models.CharField(max_length=50, null=True, blank=True)
    target_repr = models.CharField(
        max_length=255, blank=True, help_text="Human-readable snapshot of the target at the time of the action."
    )
    changes = models.JSONField(
        null=True, blank=True, help_text="Optional structured detail — e.g. {'from': 'active', 'to': 'exited'}."
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["target_type", "target_id"]),
            models.Index(fields=["action"]),
        ]

    def __str__(self):
        return f"[{self.timestamp:%Y-%m-%d %H:%M}] {self.actor} — {self.action} — {self.target_repr}"

    def save(self, *args, **kwargs):
        # Immutable: entries can be created, never edited. If code somewhere
        # tries to re-save an existing row, that's a bug worth surfacing
        # loudly rather than silently allowing history to be rewritten.
        if self.pk is not None:
            raise ValueError("AuditLog entries are immutable and cannot be updated.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValueError("AuditLog entries are immutable and cannot be deleted.")
