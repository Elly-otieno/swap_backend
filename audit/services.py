def log_audit(msisdn, event, metadata=None):
    from .models import AuditLog
    AuditLog.objects.create(
        msisdn=msisdn,
        event=event,
        metadata=metadata
    )
