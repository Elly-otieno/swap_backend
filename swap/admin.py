from django.contrib import admin
from .models import SwapSession

@admin.register(SwapSession)
class SwapSessionAdmin(admin.ModelAdmin):
    list_display = (
        "line",
        "stage",
        "primary_attempts",
        "secondary_attempts",
        "face_attempts",
        "id_attempts",
        "is_locked",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "stage",
        "is_locked",
    )

    search_fields = ("line__msisdn",)

    readonly_fields = ("created_at", "updated_at")

