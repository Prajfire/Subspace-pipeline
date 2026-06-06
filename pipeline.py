#!/usr/bin/env python3
"""
Automated Cold-Outreach Pipeline
Vocallabs/Subspace SDE Intern Assignment

Flow: seed domain → Ocean.io → Prospeo → Eazyreach → Brevo
"""

import sys
import json
from stages.ocean import find_lookalikes
from stages.prospeo import find_decision_makers
from stages.eazyreach import resolve_emails
from stages.brevo import send_outreach
from utils.logger import log, log_summary
from utils.checkpoint import safety_checkpoint


def run_pipeline(seed_domain: str):
    log(f"\n🚀 Starting outreach pipeline for: {seed_domain}\n")

    # ── Stage 1: Ocean.io ──────────────────────────────────────────
    log("📡 Stage 1/4 — Finding lookalike companies via Ocean.io...")
    lookalike_domains = find_lookalikes(seed_domain)
    if not lookalike_domains:
        log("❌ No lookalike companies found. Exiting.")
        return
    log(f"✅ Found {len(lookalike_domains)} lookalike companies.\n")

    # ── Stage 2: Prospeo ───────────────────────────────────────────
    log("🔍 Stage 2/4 — Finding decision-makers via Prospeo...")
    prospects = find_decision_makers(lookalike_domains)
    if not prospects:
        log("❌ No decision-makers found. Exiting.")
        return
    log(f"✅ Found {len(prospects)} prospects with LinkedIn URLs.\n")

    # ── Stage 3: Eazyreach ─────────────────────────────────────────
    log("📧 Stage 3/4 — Resolving work emails via Eazyreach...")
    contacts = resolve_emails(prospects)
    if not contacts:
        log("❌ No verified emails resolved. Exiting.")
        return
    log(f"✅ Resolved {len(contacts)} verified work emails.\n")

    # ── Safety Checkpoint ──────────────────────────────────────────
    log_summary(contacts)
    if not safety_checkpoint(contacts):
        log("🛑 Pipeline aborted by user before sending emails.")
        return

    # ── Stage 4: Brevo ─────────────────────────────────────────────
    log("\n📨 Stage 4/4 — Sending personalized outreach via Brevo...")
    results = send_outreach(contacts)
    
    sent     = sum(1 for r in results if r["status"] == "sent")
    failed   = sum(1 for r in results if r["status"] == "failed")
    log(f"\n✅ Pipeline complete! Sent: {sent} | Failed: {failed}")

    # Save run log
    with open("pipeline_run_log.json", "w") as f:
        json.dump({"seed_domain": seed_domain, "results": results}, f, indent=2)
    log("📄 Full run log saved to pipeline_run_log.json")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python pipeline.py <company.domain>")
        print("Example: python pipeline.py stripe.com")
        sys.exit(1)
    run_pipeline(sys.argv[1].strip().lower())
