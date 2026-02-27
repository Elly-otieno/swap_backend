from django.db import models

from django.db import models
from customers.models import Customer

class Line(models.Model):
    STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("SUSPENDED", "Suspended"),
        ("IDLE", "Idle"),
    ]

    msisdn = models.CharField(max_length=15, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    is_golden_number = models.BooleanField(default=False)
    is_whitelisted = models.BooleanField(default=False)
    is_prepaid = models.BooleanField(default=True)
    is_roaming = models.BooleanField(default=False)
    on_in_data = models.BooleanField(default=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    last_swap_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.msisdn

