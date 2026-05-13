# security/security.py
# Role 3 - Sami
# Cyber Pack security helpers: safe input validation and audit logging.

from datetime import datetime

AUDIT_LOG_FILE = "audit_log.txt"
audit_log_path = AUDIT_LOG_FILE  # exported for main.py


def _clean_log_text(value):
    if value is None:
        return ""
    return str(value).replace("\n", " ").replace("\r", " ").strip()


def log_event(event_type, detail="", result=""):
    """Write one timestamped event to audit_log.txt."""
    timestamp  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    event_type = _clean_log_text(event_type) or "EVENT"
    detail     = _clean_log_text(detail)
    result     = _clean_log_text(result)

    parts = [timestamp, event_type]
    if result:
        parts.append(result)
    if detail:
        parts.append(detail)

    try:
        with open(AUDIT_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(" - ".join(parts) + "\n")
        return True
    except OSError:
        return False


def get_valid_number(prompt, minimum, maximum, *, allow_quit=False, quit_values=None):
    """Ask for a number in range, re-prompt on bad input."""
    if minimum > maximum:
        raise ValueError("minimum cannot be greater than maximum")

    if quit_values is None:
        quit_values = ()
    normalized = {str(v).strip().upper() for v in quit_values}

    while True:
        raw = input(prompt).strip()
        raw_upper = raw.upper()

        if allow_quit and raw_upper in normalized:
            log_event("INPUT", detail=f"Special='{raw_upper}'", result="SUCCESS")
            return raw_upper

        try:
            choice = int(raw)
        except ValueError:
            print(f"Invalid input. Please enter a number from {minimum} to {maximum}.")
            log_event("INPUT_INVALID", detail=f"Expected {minimum}-{maximum}, got '{raw}'", result="FAIL")
            continue

        if minimum <= choice <= maximum:
            return choice

        print(f"Invalid choice. Please enter a number from {minimum} to {maximum}.")
        log_event("INPUT_INVALID", detail=f"Out of range '{raw}'", result="FAIL")


def get_yes_or_no(prompt):
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Invalid input. Please enter Y or N.")
        log_event("INPUT_INVALID", detail=f"Expected Y/N, got '{answer}'", result="FAIL")


def pause(message="Press Enter to continue..."):
    try:
        input(message)
    except (EOFError, KeyboardInterrupt):
        log_event("INPUT_INTERRUPTED", detail="Pause interrupted", result="FAIL")
