from django.db import models
from customers.models import Customer

class SwapSession(models.Model):
    STAGES = [
        ("STARTED", "Started"),
        ("PRIMARY_FAILED", "Primary Failed"),
        ("PRIMARY_PASSED", "Primary Passed"),
        ("DIDIT_PENDING", "Didit Pending"),
        ("DIDIT_FAILED", "Didit Failed"),
        ("DIDIT_PASSED", "Didit Passed"),
        # ("SECONDARY_FAILED", "Secondary Failed"),
        # ("SECONDARY_PASSED", "Secondary Passed"),
        # ("FACE_FAILED", "Face Failed"),
        # ("FACE_PASSED", "Face Passed"),
        # ("ID_FAILED", "ID Failed"),
        # ("ID_PASSED", "ID Passed"),
        ("COMPLETED", "Completed"),
        ("LOCKED", "Locked"),
    ]

    # customer = models.ForeignKey(Customer, 
    #     null=True, 
    #     blank=True, on_delete=models.CASCADE)

    line = models.ForeignKey("lines.Line", on_delete=models.CASCADE)
    stage = models.CharField(max_length=50, choices=STAGES)

    primary_attempts = models.IntegerField(default=0)
    secondary_attempts = models.IntegerField(default=0)
    face_attempts = models.IntegerField(default=0)
    id_attempts = models.IntegerField(default=0)

    is_locked = models.BooleanField(default=False)

    didit_session_id = models.CharField(max_length=255, null=True, blank=True)
    didit_status = models.CharField(max_length=50, null=True, blank=True)
    didit_payload = models.JSONField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

