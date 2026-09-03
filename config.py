import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
DATABASE_URL      = os.getenv("DATABASE_URL", "postgresql://localhost/shipandearn")
SECRET_KEY        = os.getenv("SECRET_KEY", "dev-secret-change-in-production")

STRIPE_SECRET_KEY     = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
STRIPE_PRICE_LIFETIME = os.getenv("STRIPE_PRICE_LIFETIME", "")
STRIPE_PRICE_PRO      = os.getenv("STRIPE_PRICE_PRO", "")

# Promo pricing (flash sale on lifetime, trial+discount on Pro).
# Both windows are config-driven so they can be started, extended, or ended
# at any time without a code change — set the *_PROMO_END date to control it.
STRIPE_PRICE_LIFETIME_PROMO    = os.getenv("STRIPE_PRICE_LIFETIME_PROMO", "")
STRIPE_PRICE_LIFETIME_STANDARD = os.getenv("STRIPE_PRICE_LIFETIME_STANDARD", "")
LIFETIME_PROMO_END             = os.getenv("LIFETIME_PROMO_END", "2026-09-30")

STRIPE_PRICE_PRO_PROMO = os.getenv("STRIPE_PRICE_PRO_PROMO", "")
PRO_PROMO_END           = os.getenv("PRO_PROMO_END", "2026-09-30")
PRO_TRIAL_DAYS          = int(os.getenv("PRO_TRIAL_DAYS", "14"))
