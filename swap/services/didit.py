import requests
from django.conf import settings
import hmac
import hashlib
from django.db import transaction

DIDIT_URL = "https://verification.didit.me/v3/session/"

def create_didit_session(session):
    payload = {
        "workflow_id": settings.DIDIT_WORKFLOW_ID,
        "callback": settings.DIDIT_CALLBACK_URL,
        "vendor_data": str(session.id),
        "redirect_url": f"swap://kyc-complete?session_id={session.id}",
        "external_id": str(session.id),
    }

    headers = {
        "x-api-key": settings.DIDIT_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(DIDIT_URL, json=payload, headers=headers, timeout=10)

    if response.status_code != 201:
        print("DIDIT ERROR:", response.status_code, response.text)
        raise Exception("Didit session creation failed")

    data = response.json()
    
    with transaction.atomic():
        session.didit_session_id = data.get("session_id")
        session.stage = "DIDIT_PENDING"
        session.save()

    return data

def verify_didit_signature(request):
    received_signature = request.headers.get("X-Signature")
    if not received_signature:
        return False

    expected_signature = hmac.new(
        settings.DIDIT_WEBHOOK_SECRET.encode(),
        request.body,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(received_signature, expected_signature)