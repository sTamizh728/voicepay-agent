import sys
from paypal_client import get_payout_status

if len(sys.argv) < 2:
    print("Usage: python check_status.py <batch_id>")
    sys.exit(1)

batch_id = sys.argv[1]
print("Status:", get_payout_status(batch_id))