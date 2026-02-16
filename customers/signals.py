from django.db.models.signals import post_save
from django.dispatch import receiver
from customers.models import Customer
from lines.models import Line
from wallet.models import WalletProfile


@receiver(post_save, sender=Customer)
def create_related_objects(sender, instance, created, **kwargs):
    if created:
        Line.objects.create(
            msisdn=instance.msisdn,
            customer=instance,
            status="ACTIVE",
            is_prepaid=True,
            is_roaming=False,
            on_in_data=True,
        )

        WalletProfile.objects.create(
            customer=instance,
            mpesa_balance=0.00,
            airtime_balance=0.00,
        )
