# security/save_load.py
# Role 3 - Sami
# Save/load system with SHA-256 tamper detection.

import hashlib
import json
import os

try:
    from security.security import log_event
except ImportError:
    def log_event(event_type, detail="", result=""):
        return False

SAVE_FILE = "savegame.json"
REQUIRED_STATE_KEYS = ("current_scene", "health", "inventory", "flags")


def _make_stable_json(data):
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _make_hash(game_state):
    return hashlib.sha256(_make_stable_json(game_state).encode("utf-8")).hexdigest()


def _is_valid_game_state(game_state):
    if not isinstance(game_state, dict):
        return False
    for key in REQUIRED_STATE_KEYS:
        if key not in game_state:
            return False
    if not isinstance(game_state.get("current_scene"), str):
        return False
    if not isinstance(game_state.get("health"), int):
        return False
    if not isinstance(game_state.get("inventory"), list):
        return False
    if not isinstance(game_state.get("flags"), dict):
        return False
    return True


def save_game(game_state, file_name=SAVE_FILE):
    if not _is_valid_game_state(game_state):
        log_event("SAVE_ATTEMPT", detail="Reason=InvalidGameState", result="FAIL")
        print("  Save failed. Game state was invalid.")
        return False
    try:
        save_data = {"game_state": game_state, "hash": _make_hash(game_state)}
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(save_data, f, indent=4, ensure_ascii=False)
        log_event("SAVE_ATTEMPT", detail=f"File={file_name}", result="SUCCESS")
        return True
    except (TypeError, OSError) as error:
        log_event("SAVE_ATTEMPT", detail=f"Error={error}", result="FAIL")
        print("  Save failed.")
        return False


def load_game(file_name=SAVE_FILE):
    if not os.path.exists(file_name):
        log_event("LOAD_ATTEMPT", detail="Reason=FileNotFound", result="FAIL")
        print("  No save file found.")
        return None
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            save_data = json.load(f)
    except json.JSONDecodeError:
        log_event("LOAD_ATTEMPT", detail="Reason=InvalidJSON", result="FAIL")
        print("  Save file is damaged.")
        return None
    except OSError as error:
        log_event("LOAD_ATTEMPT", detail=f"Error={error}", result="FAIL")
        print("  Could not read save file.")
        return None

    if not isinstance(save_data, dict):
        log_event("LOAD_ATTEMPT", detail="Reason=InvalidFormat", result="FAIL")
        return None

    game_state = save_data.get("game_state")
    saved_hash = save_data.get("hash")

    if not isinstance(saved_hash, str) or not _is_valid_game_state(game_state):
        log_event("LOAD_ATTEMPT", detail="Reason=MissingData", result="FAIL")
        print("  Save file is missing required data.")
        return None

    if _make_hash(game_state) != saved_hash:
        log_event("LOAD_ATTEMPT", detail="Reason=SAVE_TAMPERED", result="FAIL")
        print("  Save file was tampered with. Load rejected.")
        return None

    log_event("LOAD_ATTEMPT", detail=f"File={file_name}", result="SUCCESS")
    return game_state
