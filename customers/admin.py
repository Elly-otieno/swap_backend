from django.contrib import admin
from .models import Customer
from wallet.models import WalletProfile
from lines.models import Line
from swap.models import SwapSession


class LineInline(admin.TabularInline):
    model = Line
    extra = 0

class WalletInline(admin.StackedInline):
    model = WalletProfile
    extra = 0

# class SwapInline(admin.StackedInline):
#     model = SwapSession
#     extra = 0


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    inlines = [WalletInline, LineInline]
    list_display = (
        "msisdn",
        "full_name",
        "id_number",
        "yob",
        "iprs_verified",
        "iprs_approved",
        "fraud_location",
        "created_at",
        'id_photo',
    )

    search_fields = ("msisdn", "id_number", "full_name")

    list_filter = (
        "fraud_location",
        "iprs_verified",
        "iprs_approved",
    )

    readonly_fields = ("created_at",)

