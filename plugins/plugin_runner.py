import importlib

PLUGIN_MAP = {
    "payhip_bot": "plugins.payhip_bot",
    "paypal_api": "payment.paypal_api",
    "gumroad_bot": "plugins.gumroad_bot",
    "sellfy_bot": "plugins.sellfy_bot",
    "etsy_bot": "plugins.etsy_bot",
    "shopify_bot": "plugins.shopify_bot",
    "podia_bot": "plugins.podia_bot",
    
    "instagram": "marketing.instagram",
    "tiktok": "marketing.tiktok",
    "facebook": "marketing.facebook",
    "linkedin": "marketing.linkedin",
    "pinterest": "marketing.pinterest",
    "reddit": "marketing.reddit",
    "youtube": "marketing.youtube",

    "mailchimp_api": "email.mailchimp_api",
    "sendinblue_api": "email.sendinblue_api",
    "convertkit_api": "email.convertkit_api",
    "activecampaign_api": "email.activecampaign_api",

    "hubspot": "crm.hubspot",
    "notion_api": "knowledge.notion_api",
    "scraper": "scrapers.web_scraper",
}

def run_plugin(plugin, action, args):
    module_path = PLUGIN_MAP.get(plugin)
    if not module_path:
        raise ValueError(f"🔌 Plugin inconnu ou non mappé : {plugin}")
    
    try:
        module = importlib.import_module(module_path)
        if not hasattr(module, "handle_action"):
            raise AttributeError(f"Le module {plugin} ne contient pas de fonction 'handle_action'")
        return module.handle_action(action, args)
    
    except Exception as e:
        print(f"[❌ Erreur PluginRunner] Plugin: {plugin}, Action: {action}, Erreur: {e}")
        raise e
