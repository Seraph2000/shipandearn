import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
DATABASE_URL      = os.getenv("DATABASE_URL", "postgresql://localhost/earnstack")
SECRET_KEY        = os.getenv("SECRET_KEY", "dev-secret-change-in-production")
