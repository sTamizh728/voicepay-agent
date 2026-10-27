import sys
from paypal_client import get_payout_status

batch_id = sys.argv[1]  # the batch ID you type after the file name
print("Status:", get_payout_status(batch_id))