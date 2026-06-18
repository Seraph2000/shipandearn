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
