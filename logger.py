# utils/logger.py
from datetime import datetime


def log(message: str):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {message}")


def log_summary(contacts: list[dict]):
    print("\n" + "="*55)
    print("  📋 OUTREACH SUMMARY — REVIEW BEFORE SENDING")
    print("="*55)
    print(f"  Total contacts ready to email: {len(contacts)}\n")
    for i, c in enumerate(contacts, 1):
        print(f"  {i:>2}. {c['full_name']:<28} {c.get('title',''):<25}")
        print(f"      Email: {c['email']}")
        print(f"      Company: {c['company']}")
        print()
    print("="*55)
