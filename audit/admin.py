from django.contrib import admin
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = (
        "msisdn",
        "event",
        "created_at",
    )

    search_fields = ("msisdn", "event")

    readonly_fields = ("created_at",)

