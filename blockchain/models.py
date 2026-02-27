import hashlib
import json
from django.db import models

# tamper proof append only table
class Block(models.Model):
    index = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    event = models.CharField(max_length=255)
    msisdn = models.CharField(max_length=15)
    previous_hash = models.CharField(max_length=256)
    hash = models.CharField(max_length=256)

    def calculate_hash(self):
        data = f"{self.index}{self.timestamp}{self.event}{self.msisdn}{self.previous_hash}"
        return hashlib.sha256(data.encode()).hexdigest()

class BlockchainTransaction(models.Model):
    tx_hash = models.CharField(max_length=100, unique=True)
    contract_address = models.CharField(max_length=42)
    function_name = models.CharField(max_length=50)
    user_id = models.CharField(max_length=100, null=True, blank=True)
    request_id = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20, default='PENDING') # PENDING, CONFIRMED, FAILED
    block_number = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.function_name} ({self.tx_hash[:10]}...)"
