


# import requests

# def send_campaign(api_key, list_id, subject, content):
#     url = f"https://<dc>.api.mailchimp.com/3.0/campaigns"
#     headers = {"Authorization": f"apikey {api_key}"}
#     # Exemple basique (voir docs Mailchimp pour détails complets)
#     data = {
#         "type": "regular",
#         "recipients": {"list_id": list_id},
#         "settings": {
#             "subject_line": subject,
#             "title": subject,
#             "from_name": "AutomateBot",
#             "reply_to": "noreply@example.com"
#         }
#     }
#     r = requests.post(url, headers=headers, json=data)
#     if r.status_code == 200:
#         campaign_id = r.json()["id"]
#         content_url = f"https://<dc>.api.mailchimp.com/3.0/campaigns/{campaign_id}/content"
#         requests.put(content_url, headers=headers, json={"html": content})
#         requests.post(f"https://<dc>.api.mailchimp.com/3.0/campaigns/{campaign_id}/actions/send", headers=headers)
#         print("✅ Campagne Mailchimp envoyée")
#     else:
#         print("❌ Erreur Mailchimp", r.text)




import requests

def send_campaign(api_key, server_prefix, list_id, subject, content):
    headers = {
        "Authorization": f"apikey {api_key}",
        "Content-Type": "application/json"
    }
    campaign_url = f"https://{server_prefix}.api.mailchimp.com/3.0/campaigns"
    create_resp = requests.post(campaign_url, headers=headers, json={
        "type": "regular",
        "recipients": {"list_id": list_id},
        "settings": {"subject_line": subject, "title": subject, "from_name": "Bot", "reply_to": "you@example.com"}
    })
    cid = create_resp.json().get("id")
    content_url = f"{campaign_url}/{cid}/content"
    requests.put(content_url, headers=headers, json={"html": content})
    requests.post(f"{campaign_url}/{cid}/actions/send", headers=headers)
    print("✅ Campagne envoyée via Mailchimp")

    
