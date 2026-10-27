import os
import httpx
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("PAYPAL_CLIENT_ID")
secret = os.getenv("PAYPAL_SECRET")
base_url = os.getenv("PAYPAL_BASE_URL")

# Ask PayPal for an access token using our app's keys
response = httpx.post(
    f"{base_url}/v1/oauth2/token",
    auth=(client_id, secret),
    data={"grant_type": "client_credentials"},
)

if response.status_code == 200:
    print("SUCCESS: PayPal keys work!")
    print("Token expires in", response.json()["expires_in"], "seconds")
else:
    print("FAILED:", response.status_code, response.text)