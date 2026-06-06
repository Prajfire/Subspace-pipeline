# utils/checkpoint.py — Safety gate before emails fire
from utils.logger import log


def safety_checkpoint(contacts: list[dict]) -> bool:
    """
    Show a summary of who will be emailed and ask for explicit confirmation.
    This is the required safety checkpoint before the pipeline fires emails.
    Returns True to proceed, False to abort.
    """
    log(f"\n⚠️  About to send {len(contacts)} emails. This cannot be undone.")
    log("   Type 'yes' to confirm and send, anything else to abort:")
    
    answer = input("   > ").strip().lower()
    return answer == "yes"
