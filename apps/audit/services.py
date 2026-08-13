def _client_ip(request):
    if request is None:
        return None
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def log_action(actor, action, target=None, changes=None, request=None):
    """
    Write one immutable audit entry.

    actor:   the User performing the action (None for system-initiated events)
    action:  short slug, e.g. "employee.exited", "document.archived"
    target:  the model instance the action was performed on (optional)
    changes: optional JSON-serializable dict of what changed
    request: optional DRF/Django request, used only to capture the IP

    Deliberately swallows nothing — if this raises (e.g. bad `changes`
    value that isn't JSON-serializable), that should surface during
    development rather than silently dropping an audit record.
    """
    from .models import AuditLog

    target_type = ""
    target_id = None
    target_repr = ""
    if target is not None:
        target_type = f"{target._meta.app_label}.{target._meta.object_name}"
        target_id = str(target.pk)
        target_repr = str(target)[:255]

    AuditLog.objects.create(
        actor=actor,
        action=action,
        target_type=target_type,
        target_id=target_id,
        target_repr=target_repr,
        changes=changes,
        ip_address=_client_ip(request),
    )
