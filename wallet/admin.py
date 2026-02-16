from django.contrib import admin
from .models import WalletProfile

@admin.register(WalletProfile)
class WalletProfileAdmin(admin.ModelAdmin):
    list_display = (
        "customer",
        "mpesa_balance",
        "airtime_balance",
        "fuliza_limit",
        "fuliza_opted_in",
        "mshwari_limit",
        "mshwari_opted_in",
        "kcb_limit",
        "kcb_opted_in",
    )

    list_filter = (
        "fuliza_opted_in",
        "mshwari_opted_in",
        "kcb_opted_in",
    )

    search_fields = ("customer__msisdn",)

