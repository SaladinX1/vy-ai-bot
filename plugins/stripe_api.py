import stripe
import os

stripe.api_key = os.getenv("STRIPE_API_KEY")

def create_payment_link(product_name, amount_cents, currency="usd"):
    try:
        product = stripe.Product.create(name=product_name)
        price = stripe.Price.create(
            product=product.id,
            unit_amount=amount_cents,
            currency=currency,
        )
        payment_link = stripe.PaymentLink.create(
            line_items=[{"price": price.id, "quantity": 1}],
        )
        return payment_link.url
    except Exception as e:
        print(f"Erreur Stripe: {e}")
        return None

if __name__ == "__main__":
    url = create_payment_link("Ebook Gestion Temps Freelance", 1500)
    print(f"Payment Link: {url}")
