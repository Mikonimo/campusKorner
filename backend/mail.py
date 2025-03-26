import requests
import json
from config import MAILCHIMP_API_KEY, MAILCHIMP_SERVER_PREFIX, MAILCHIMP_LIST_ID


def add_subscriber(email, first_name, last_name):
    url = f"https://{MAILCHIMP_SERVER_PREFIX}.api.mailchimp.com/3.0/lists/{MAILCHIMP_LIST_ID}/members"

    headers = {
        "Authorization": f"apikey {MAILCHIMP_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "email_address": email,
        "status": "subscribed",  # or "pending" if you want double opt-in
        "merge_fields": {
            "FNAME": first_name,
            "LNAME": last_name
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    return response.json()
