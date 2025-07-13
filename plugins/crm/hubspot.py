class HubSpotCRM:
    def add_contact(self, email, name):
        # Requiert HubSpot API Key
        url = "https://api.hubapi.com/contacts/v1/contact"
        payload = {
            "properties": [
                {"property": "email", "value": email},
                {"property": "firstname", "value": name}
            ]
        }
        # requests.post(url, headers={...}, json=payload)
        pass