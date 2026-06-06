# Automated Cold-Outreach Pipeline
### Vocallabs / Subspace SDE Intern Assignment

A single command-line program that automates the entire cold outreach pipeline — from one seed domain to sent emails — with zero manual steps in between.

---

## Architecture

```
python pipeline.py stripe.com
        │
        ▼
[Stage 1] Ocean.io     → finds lookalike company domains
        │
        ▼
[Stage 2] Prospeo      → finds C-suite/VP names + LinkedIn URLs per domain
        │
        ▼
[Stage 3] Eazyreach    → resolves LinkedIn URLs → verified work emails
        │
        ▼
  ⚠️  Safety Checkpoint  → shows full contact list, asks for confirmation
        │
        ▼
[Stage 4] Brevo        → sends personalized outreach email to each contact
```

---

## Setup

### 1. Prerequisites (do these in order)

| Step | Action |
|------|--------|
| 1 | Buy/claim a domain (Namecheap or GitHub Student Pack) |
| 2 | Create a company email `you@yourdomain.com` via Brevo |
| 3 | Sign up at **ocean.io** using that company email |
| 4 | Sign up at **app.prospeo.io** |
| 5 | Sign up at **eazyreach.app** (ask team to top up credits) |
| 6 | Sign up at **app.brevo.com** |

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API keys

```bash
cp .env.example .env
# Edit .env and fill in all your API keys
```

### 4. Run the pipeline

```bash
python pipeline.py <seed_domain>

# Example:
python pipeline.py stripe.com
```

---

## How It Works

### Stage 1 — Ocean.io
Sends the seed domain to Ocean.io's lookalike/similarity API. Returns up to 10 similar company domains.

### Stage 2 — Prospeo  
For each domain, calls Prospeo's domain-search API to surface C-suite and VP-level contacts along with their LinkedIn profile URLs.

### Stage 3 — Eazyreach
For each LinkedIn URL, calls Eazyreach to resolve and verify the person's work email address. Skips contacts where Prospeo already returned an email.

### Stage 4 — Brevo
Composes a personalized email for each contact (using their first name, title, and company) and sends it via Brevo's transactional email API.

### Safety Checkpoint
Before Stage 4 fires, the pipeline prints a full summary of all contacts and asks for explicit `yes` confirmation. This prevents accidental bulk sends.

---

## Edge Cases Handled

| Scenario | Handling |
|----------|----------|
| No lookalikes found | Pipeline exits cleanly after Stage 1 |
| Domain has no C-suite contacts | Skipped, pipeline continues with remaining domains |
| LinkedIn URL missing | Contact skipped in Stage 3, logged |
| Email already in Prospeo response | Eazyreach call skipped (saves credits) |
| Eazyreach can't resolve email | Contact excluded from final send list |
| Rate limits | 0.3–0.5s delay between calls per stage |
| API HTTP errors | Caught, logged, pipeline continues |
| User aborts at checkpoint | Clean exit before any emails are sent |

---

## Output

- **Console logs** with timestamps for every step
- **pipeline_run_log.json** saved after each run with full results

---

## File Structure

```
outreach_pipeline/
├── pipeline.py          # Entry point — orchestrates all 4 stages
├── config.py            # API keys + settings (loaded from .env)
├── requirements.txt
├── .env.example
├── stages/
│   ├── ocean.py         # Stage 1: Ocean.io lookalike search
│   ├── prospeo.py       # Stage 2: Prospeo decision-maker search
│   ├── eazyreach.py     # Stage 3: Email resolution
│   └── brevo.py         # Stage 4: Email sending + copy
└── utils/
    ├── logger.py        # Console logging + summary table
    └── checkpoint.py    # Safety gate before emails fire
```
