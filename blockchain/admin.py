from django.contrib import admin
from .models import Block

@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = (
        "index",
        "timestamp",
        "event",
        "msisdn",
        "previous_hash",
        "hash",
    )
    list_filter = ("timestamp", "event")
    search_fields = ("event", "msisdn", "hash", "previous_hash")
    ordering = ("index",)

    readonly_fields = ("timestamp", "hash")

    def save_model(self, request, obj, form, change):
        # Automatically calculate hash before saving
        obj.hash = obj.calculate_hash()
        super().save_model(request, obj, form, change)
