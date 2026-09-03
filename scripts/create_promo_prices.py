"""
One-off script to create the new Stripe Price objects needed for the
lifetime flash sale (£1.99, then £6.99 standard) and the Pro trial promo
(£7.99/mo, reverting to the existing STRIPE_PRICE_PRO price after the promo).

Stripe Prices are immutable, so these are new objects attached to the
existing Products (looked up from the current STRIPE_PRICE_LIFETIME and
STRIPE_PRICE_PRO price IDs) — this does not touch or archive any existing
price, so current subscribers/checkout links are unaffected.

Usage:
    python scripts/create_promo_prices.py

Requires STRIPE_SECRET_KEY, STRIPE_PRICE_LIFETIME, STRIPE_PRICE_PRO to
already be set (via .env). Prints the new price_... IDs to paste into
STRIPE_PRICE_LIFETIME_PROMO, STRIPE_PRICE_LIFETIME_STANDARD, and
STRIPE_PRICE_PRO_PROMO.
"""
import stripe
import config

stripe.api_key = config.STRIPE_SECRET_KEY

if not config.STRIPE_SECRET_KEY:
    raise SystemExit("STRIPE_SECRET_KEY is not set")
if not config.STRIPE_PRICE_LIFETIME:
    raise SystemExit("STRIPE_PRICE_LIFETIME is not set")
if not config.STRIPE_PRICE_PRO:
    raise SystemExit("STRIPE_PRICE_PRO is not set")

lifetime_product = stripe.Price.retrieve(config.STRIPE_PRICE_LIFETIME).product
pro_product      = stripe.Price.retrieve(config.STRIPE_PRICE_PRO).product

lifetime_promo = stripe.Price.create(
    product=lifetime_product,
    unit_amount=199,
    currency="gbp",
    nickname="Lifetime — flash sale £1.99",
)
lifetime_standard = stripe.Price.create(
    product=lifetime_product,
    unit_amount=699,
    currency="gbp",
    nickname="Lifetime — standard £6.99",
)
pro_promo = stripe.Price.create(
    product=pro_product,
    unit_amount=799,
    currency="gbp",
    recurring={"interval": "month"},
    nickname="Pro — trial promo £7.99/mo",
)

print("Add these to .env:")
print(f"STRIPE_PRICE_LIFETIME_PROMO={lifetime_promo.id}")
print(f"STRIPE_PRICE_LIFETIME_STANDARD={lifetime_standard.id}")
print(f"STRIPE_PRICE_PRO_PROMO={pro_promo.id}")
