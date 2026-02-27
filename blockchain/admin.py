from django.contrib import admin
from .models import Block, BlockchainTransaction

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


@admin.register(BlockchainTransaction)
class BlockchainTransactionAdmin(admin.ModelAdmin):
    list_display = (
        'tx_hash_short', 
        'function_name', 
        'status', 
        'user_id', 
        'block_number', 
        'created_at', 
        'confirmed_at'
    )

    list_filter = ('status', 'function_name', 'created_at')
    search_fields = ('tx_hash', 'contract_address', 'user_id', 'request_id')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

    @admin.display(description='Transaction Hash')
    def tx_hash_short(self, obj):
        return f"{obj.tx_hash[:12]}..." if obj.tx_hash else "-"