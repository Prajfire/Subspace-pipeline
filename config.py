# config.py — Set your API keys here (or use a .env file)
import os
from dotenv import load_dotenv

load_dotenv()

# ── Ocean.io ────────────────────────────────────────────────
OCEAN_API_KEY    = os.getenv("OCEAN_API_KEY", "YOUR_OCEAN_API_KEY")
OCEAN_LOOKALIKE_LIMIT = int(os.getenv("OCEAN_LOOKALIKE_LIMIT", "10"))

# ── Prospeo ─────────────────────────────────────────────────
PROSPEO_API_KEY  = os.getenv("PROSPEO_API_KEY", "YOUR_PROSPEO_API_KEY")
PROSPEO_ROLES    = ["CEO", "CTO", "COO", "VP", "Director", "Head of"]

# ── Eazyreach ────────────────────────────────────────────────
EAZYREACH_API_KEY = os.getenv("EAZYREACH_API_KEY", "YOUR_EAZYREACH_API_KEY")

# ── Brevo ────────────────────────────────────────────────────
BREVO_API_KEY    = os.getenv("BREVO_API_KEY", "YOUR_BREVO_API_KEY")
SENDER_EMAIL     = os.getenv("SENDER_EMAIL", "you@yourdomain.com")
SENDER_NAME      = os.getenv("SENDER_NAME", "Your Name")
