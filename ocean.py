# stages/ocean.py — Stage 1: Find lookalike companies via Ocean.io
import requests
from config import OCEAN_API_KEY, OCEAN_LOOKALIKE_LIMIT
from utils.logger import log


def find_lookalikes(seed_domain: str) -> list[str]:
    """
    Given a seed company domain, return a list of lookalike company domains
    using Ocean.io's similarity search API.
    """
    url = "https://api.ocean.io/v1/lookalikes"
    headers = {
        "Authorization": f"Bearer {OCEAN_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "domain": seed_domain,
        "limit": OCEAN_LOOKALIKE_LIMIT,
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()

        # Ocean.io returns companies in data["companies"] or similar
        companies = data.get("companies", data.get("results", []))
        domains = []

        for company in companies:
            domain = company.get("domain") or company.get("website", "")
            # Clean up domain (strip http/https/www)
            domain = domain.replace("https://", "").replace("http://", "").replace("www.", "").strip("/")
            if domain:
                domains.append(domain)
                log(f"  → {domain} ({company.get('name', 'Unknown')})")

        return domains

    except requests.exceptions.HTTPError as e:
        log(f"  ⚠️  Ocean.io HTTP error: {e.response.status_code} — {e.response.text}")
        return []
    except requests.exceptions.RequestException as e:
        log(f"  ⚠️  Ocean.io connection error: {e}")
        return []
    except (KeyError, ValueError) as e:
        log(f"  ⚠️  Ocean.io response parse error: {e}")
        return []
