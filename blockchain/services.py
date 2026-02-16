import requests

RUST_BLOCKCHAIN_URL = "http://localhost:8001/log"

def log_event(event, msisdn):
    payload = {
        "event": event,
        "msisdn": msisdn
    }
    requests.post(RUST_BLOCKCHAIN_URL, json=payload)
