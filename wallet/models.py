from django.db import models

from django.db import models
from customers.models import Customer

class WalletProfile(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)

    mpesa_balance = models.DecimalField(max_digits=12, decimal_places=2)
    airtime_balance = models.DecimalField(max_digits=12, decimal_places=2)

    fuliza_limit = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    fuliza_opted_in = models.BooleanField(default=False)

    mshwari_limit = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    mshwari_opted_in = models.BooleanField(default=False)

    kcb_limit = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    kcb_opted_in = models.BooleanField(default=False)

