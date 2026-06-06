# stages/prospeo.py — Stage 2: Find decision-makers via Prospeo
import time
import requests
from config import PROSPEO_API_KEY, PROSPEO_ROLES
from utils.logger import log


def find_decision_makers(domains: list[str]) -> list[dict]:
    """
    For each domain, find C-suite/VP contacts + their LinkedIn URLs using Prospeo.
    Returns a flat list of prospect dicts.
    """
    all_prospects = []

    for domain in domains:
        log(f"  🔎 Prospeo searching: {domain}")
        contacts = _search_domain(domain)
        if contacts:
            log(f"     Found {len(contacts)} decision-makers")
            all_prospects.extend(contacts)
        else:
            log(f"     No contacts found for {domain}")
        time.sleep(0.5)   # rate-limit courtesy

    return all_prospects


def _search_domain(domain: str) -> list[dict]:
    """Call Prospeo's domain-search endpoint."""
    url = "https://api.prospeo.io/domain-search"
    headers = {
        "X-KEY": PROSPEO_API_KEY,
        "Content-Type": "application/json",
    }
    payload = {
        "domain": domain,
        "limit": 10,
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()

        prospects = []
        for person in data.get("response", {}).get("email_list", []):
            title = person.get("position", "").lower()
            # Filter for C-suite / VP / Director level
            if any(role.lower() in title for role in PROSPEO_ROLES):
                prospects.append({
                    "first_name":    person.get("first_name", ""),
                    "last_name":     person.get("last_name", ""),
                    "full_name":     f"{person.get('first_name','')} {person.get('last_name','')}".strip(),
                    "title":         person.get("position", ""),
                    "company":       person.get("company", domain),
                    "domain":        domain,
                    "linkedin_url":  person.get("linkedin", ""),
                    "email":         person.get("email", ""),   # may already have email
                })
        return prospects

    except requests.exceptions.HTTPError as e:
        log(f"     ⚠️  Prospeo error for {domain}: {e.response.status_code}")
        return []
    except requests.exceptions.RequestException as e:
        log(f"     ⚠️  Prospeo connection error: {e}")
        return []
