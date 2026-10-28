import os
import uuid
import httpx
from dotenv import load_dotenv

load_dotenv(override=True)

CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")
SECRET = os.getenv("PAYPAL_SECRET")
BASE_URL = os.getenv("PAYPAL_BASE_URL")


def get_access_token():
    """Ask PayPal for a temporary pass (access token)."""
    response = httpx.post(
        f"{BASE_URL}/v1/oauth2/token",
        auth=(CLIENT_ID, SECRET),
        data={"grant_type": "client_credentials"},
    )
    response.raise_for_status()
    return response.json()["access_token"]


def send_payout(receiver_email, amount, note="Sent with VoicePay Agent"):
    """Send money to one person by email. Returns PayPal's batch ID."""
    token = get_access_token()
    body = {
        "sender_batch_header": {
            "sender_batch_id": str(uuid.uuid4()),  # unique ID so PayPal never sends twice
            "email_subject": "You received money via VoicePay Agent",
        },
        "items": [
            {
                "recipient_type": "EMAIL",
                "receiver": receiver_email,
                "amount": {"value": f"{amount:.2f}", "currency": "USD"},
                "note": note,
            }
        ],
    }
    response = httpx.post(
        f"{BASE_URL}/v1/payments/payouts",
        headers={"Authorization": f"Bearer {token}"},
        json=body,
    )
    response.raise_for_status()
    return response.json()["batch_header"]["payout_batch_id"]


def get_payout_status(batch_id):
    """Check whether a payout finished: PENDING, PROCESSING, SUCCESS, DENIED..."""
    token = get_access_token()
    response = httpx.get(
        f"{BASE_URL}/v1/payments/payouts/{batch_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    response.raise_for_status()
    return response.json()["batch_header"]["batch_status"]