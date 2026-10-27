import time
from paypal_client import send_payout, get_payout_status

PRIYA = "sb-oaavd53471227@business.example.com"

batch_id = send_payout(PRIYA, 1.00)
print("Payout sent! Batch ID:", batch_id)

time.sleep(5)  # give PayPal a few seconds to process
print("Status:", get_payout_status(batch_id))