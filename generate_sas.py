import base64
import hmac
import hashlib
import time
import urllib.parse

# Update these values
IOT_HUB_NAME = "<YOUR_IOT_HUB_NAME>.azure-devices.net"
DEVICE_ID = "<YOUR_DEVICE_ID>"
SHARED_ACCESS_KEY = "<DEVICE_PRIMARY_KEY>"

# Token expiration (1 hour from now)
expiry = int(time.time()) + 3600

# Create the signature string
to_sign = f"{IOT_HUB_NAME}/devices/{DEVICE_ID}\n{expiry}"
signature = base64.b64encode(
    hmac.new(base64.b64decode(SHARED_ACCESS_KEY), to_sign.encode('utf-8'), hashlib.sha256).digest()
).decode()

# Encode the URL
signature = urllib.parse.quote(signature, safe='')

# Generate the final SAS token
sas_token = f"SharedAccessSignature sr={IOT_HUB_NAME}/devices/{DEVICE_ID}&sig={signature}&se={expiry}"
print(f"🔑 Your SAS Token:\n{sas_token}")
