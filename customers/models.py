from django.db import models
from swap.utils.msisdn import normalize_msisdn

class Customer(models.Model):
    FRAUD_LOCATION_CHOICES = [
        ("NORMAL", "Normal"),
        ("PRISON_SITE", "Prison Site"),
        ("DETACHED", "Detached"),
    ]

    msisdn = models.CharField(max_length=12, unique=True)
    full_name = models.CharField(max_length=255)
    id_number = models.CharField(max_length=50)
    yob = models.IntegerField()

    iprs_verified = models.BooleanField(default=False)
    iprs_approved = models.BooleanField(default=False)

    fraud_location = models.CharField(
        max_length=20,
        choices=FRAUD_LOCATION_CHOICES,
        default="NORMAL"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.msisdn = normalize_msisdn(self.msisdn)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.msisdn

