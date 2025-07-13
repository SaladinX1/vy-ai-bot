# plugins/payhip_bot.py

from vision.actions import click_text, type_text, wait_for_element

class PayhipBot:
    def create_account(self, email, password):
        # Automatiser la création de compte via interface (UI)
        wait_for_element("Sign up")
        click_text("Sign up")
        type_text(email)
        type_text(password)
        click_text("Create Account")

    def upload_product(self, title, description, file_path):
        # Automatiser l'ajout d'un produit digital
        click_text("Add Product")
        type_text(title)
        type_text(description)
        click_text("Upload File")
        type_text(file_path)
        click_text("Publish")

# Action handler

def handle_action(action, args):
    bot = PayhipBot()

    if action == "create_account":
        return bot.create_account(args["email"], args["password"])

    elif action == "upload_product":
        return bot.upload_product(
            title=args["title"],
            description=args["description"],
            file_path=args["file_path"]
        )

    else:
        raise ValueError(f"[Payhip] Action inconnue : {action}")
