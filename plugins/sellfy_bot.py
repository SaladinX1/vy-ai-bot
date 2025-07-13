# plugins/sellfy_bot.py

from vision.actions import click_text, type_text, wait_for_element

def add_product(args):
    title = args.get("title", "Produit Sans Titre")
    file_path = args.get("file_path", "products/default.pdf")

    print(f"[SELLFY] Ajout produit: {args}")

    click_text("Add product")
    type_text(title)
    type_text(file_path)
    click_text("Save")

    return {"status": "success", "id": "sellfy_101"}

def handle_action(action, args):
    if action == "add_product":
        return add_product(args)
    else:
        raise ValueError(f"[SELLFY] Action inconnue: {action}")
