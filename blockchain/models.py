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
