# import requests

# RUST_BLOCKCHAIN_URL = "http://localhost:8001/log"

# def log_event(event, msisdn):
#     payload = {
#         "event": event,
#         "msisdn": msisdn
#     }
#     requests.post(RUST_BLOCKCHAIN_URL, json=payload)

from blockchain.models import Block
import hashlib

def log_event(event, msisdn):
    last_block = Block.objects.order_by("-index").first()

    index = 1 if not last_block else last_block.index + 1
    previous_hash = "0" if not last_block else last_block.hash

    block = Block.objects.create(
        index=index,
        event=event,
        msisdn=msisdn,
        previous_hash=previous_hash,
        hash=""
    )

    block.hash = block.calculate_hash()
    block.save()
