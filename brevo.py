# stages/brevo.py — Stage 4: Send personalized outreach emails via Brevo
import time
import requests
from config import BREVO_API_KEY, SENDER_EMAIL, SENDER_NAME
from utils.logger import log


def send_outreach(contacts: list[dict]) -> list[dict]:
    """
    Send a personalized cold-outreach email to each contact via Brevo.
    Returns a list of result dicts with status per contact.
    """
    results = []

    for contact in contacts:
        log(f"  📤 Sending to {contact['full_name']} <{contact['email']}> @ {contact['company']}...")
        subject, html_body = _compose_email(contact)
        status = _send_single(contact["email"], contact["full_name"], subject, html_body)

        results.append({
            "name":    contact["full_name"],
            "email":   contact["email"],
            "company": contact["company"],
            "status":  status,
        })

        if status == "sent":
            log(f"     ✅ Sent")
        else:
            log(f"     ❌ Failed")

        time.sleep(0.3)  # stay within Brevo rate limits

    return results


def _compose_email(contact: dict) -> tuple[str, str]:
    """
    Compose a personalized outreach email.
    Personalization hooks: first name, title, company.
    """
    first_name = contact.get("first_name") or contact["full_name"].split()[0]
    company    = contact.get("company", "your company")
    title      = contact.get("title", "")

    subject = f"Quick question about {company}'s growth strategy"

    html_body = f"""
    <html><body style="font-family: Arial, sans-serif; font-size: 15px; color: #222; max-width: 600px;">
    <p>Hi {first_name},</p>

    <p>I came across {company} while researching fast-growing companies in your space — genuinely
    impressive what the team has built.</p>

    <p>{"As " + title + ", I imagine" if title else "I imagine"} scaling outreach and lead-gen operations
    is top of mind. We're building automation tooling that removes the manual work from prospecting —
    from finding lookalike customers to landing verified emails in the inbox, end-to-end with zero
    human touchpoints.</p>

    <p>Would a 15-minute call this week make sense? Happy to show you a live demo
    and tailor the conversation to {company}'s specific bottlenecks.</p>

    <p>Either way, keep up the great work.</p>

    <p>Best,<br>
    <strong>{SENDER_NAME}</strong><br>
    <a href="mailto:{SENDER_EMAIL}">{SENDER_EMAIL}</a></p>
    </body></html>
    """
    return subject, html_body


def _send_single(to_email: str, to_name: str, subject: str, html_body: str) -> str:
    """Call Brevo transactional email API. Returns 'sent' or 'failed'."""
    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "api-key": BREVO_API_KEY,
        "Content-Type": "application/json",
    }
    payload = {
        "sender": {"name": SENDER_NAME, "email": SENDER_EMAIL},
        "to": [{"email": to_email, "name": to_name}],
        "subject": subject,
        "htmlContent": html_body,
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return "sent"

    except requests.exceptions.HTTPError as e:
        log(f"     ⚠️  Brevo error: {e.response.status_code} — {e.response.text[:300]}")
        return "failed"
    except requests.exceptions.RequestException as e:
        log(f"     ⚠️  Brevo connection error: {e}")
        return "failed"
