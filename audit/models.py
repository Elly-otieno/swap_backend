from django.db import models

class AuditLog(models.Model):
    msisdn = models.CharField(max_length=15)
    event = models.CharField(max_length=100)
    metadata = models.JSONField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
