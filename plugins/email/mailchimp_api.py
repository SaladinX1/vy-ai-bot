

import requests

class MailchimpAPI:
    def __init__(self, api_key, list_id):
        self.api_key = api_key
        self.list_id = list_id

    def add_subscriber(self, email):
        url = f"https://usX.api.mailchimp.com/3.0/lists/{self.list_id}/members"
        data = {"email_address": email, "status": "subscribed"}
        r = requests.post(url, auth=("anystring", self.api_key), json=data)
        return r.status_code == 200
    

    def send_campaign(api_key, list_id, subject, content):
        url = f"https://<dc>.api.mailchimp.com/3.0/campaigns"
        headers = {"Authorization": f"apikey {api_key}"}
        # ... Création + contenu + envoi (voir Mailchimp API v3.0)
        print("✅ Campagne Mailchimp simulée (intégration réelle à faire)")
