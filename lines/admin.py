from django.contrib import admin
from .models import Line

@admin.register(Line)
class LineAdmin(admin.ModelAdmin):
    list_display = (
        "msisdn",
        "customer",
        "status",
        "is_golden_number",
        "is_whitelisted",
        "is_prepaid",
        "is_roaming",
        "on_in_data",
        "last_swap_at",
    )

    search_fields = ("msisdn",)

    list_filter = (
        "status",
        "is_golden_number",
        "is_whitelisted",
        "is_prepaid",
        "is_roaming",
        "on_in_data",
    )

