import os
from twilio.rest import Client
# Set environment variables for your credentials
# Read more at http://twil.io/secure
account_sid = os.environ["SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)

def send_msg():
    message = client.messages.create(
    body="Your House is on Fire",
    from_="+18447532045",
    to="+14845412289"
    )
    print(message.sid)

send_msg()