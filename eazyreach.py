# stages/eazyreach.py — Stage 3: Resolve LinkedIn URLs → verified work emails
import time
import requests
from config import EAZYREACH_API_KEY
from utils.logger import log


def resolve_emails(prospects: list[dict]) -> list[dict]:
    """
    For each prospect, resolve their LinkedIn URL into a verified work email
    via Eazyreach. Skips contacts that already have emails from Prospeo.
    Returns only contacts where email resolution succeeded.
    """
    enriched = []

    for prospect in prospects:
        # Skip if Prospeo already found the email
        if prospect.get("email"):
            log(f"  ✉️  Already have email for {prospect['full_name']} — skipping Eazyreach")
            enriched.append(prospect)
            continue

        linkedin_url = prospect.get("linkedin_url", "")
        if not linkedin_url:
            log(f"  ⚠️  No LinkedIn URL for {prospect['full_name']} ({prospect['domain']}) — skipping")
            continue

        log(f"  🔗 Resolving email for {prospect['full_name']} via Eazyreach...")
        email = _resolve_single(linkedin_url)

        if email:
            prospect["email"] = email
            log(f"     ✅ {email}")
            enriched.append(prospect)
        else:
            log(f"     ❌ Could not resolve email for {prospect['full_name']}")

        time.sleep(0.5)  # rate-limit courtesy

    return enriched


def _resolve_single(linkedin_url: str) -> str | None:
    """Call Eazyreach API to get verified work email from LinkedIn URL."""
    url = "https://api.eazyreach.app/v1/find-email"
    headers = {
        "Authorization": f"Bearer {EAZYREACH_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {"linkedin_url": linkedin_url}

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()

        # Adjust key based on actual Eazyreach response shape
        email = (
            data.get("email")
            or data.get("work_email")
            or data.get("data", {}).get("email")
        )
        return email if email else None

    except requests.exceptions.HTTPError as e:
        log(f"     ⚠️  Eazyreach HTTP error: {e.response.status_code} — {e.response.text[:200]}")
        return None
    except requests.exceptions.RequestException as e:
        log(f"     ⚠️  Eazyreach connection error: {e}")
        return None
