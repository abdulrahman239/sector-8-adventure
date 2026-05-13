# main.py
# Role 1 - Raki + Sami (merged)
# Entry point and main menu.

import os
import sys

try:
    from engine.game_engine import run_scene
except ImportError as error:
    print("Could not import engine.game_engine. Check folder structure.")
    raise error

try:
    from engine.state import create_new_state
except ImportError:
    # Fallback if state.py is empty - keeps the game runnable
    def create_new_state():
        try:
            from content.story import get_initial_flags
            flags = get_initial_flags()
        except ImportError:
            flags = {}
        return {
            "current_scene": "start",
            "health":        100,
            "max_health":    100,
            "inventory":     [],
            "flags":         flags,
        }

try:
    from security.security import (
        get_valid_number,
        get_yes_or_no,
        log_event,
        pause,
        audit_log_path,
    )
except ImportError:
    audit_log_path = "audit_log.txt"

    def log_event(event_type, detail="", result=""):
        return False

    def get_valid_number(prompt, minimum, maximum, **kwargs):
        while True:
            raw = input(prompt).strip()
            try:
                choice = int(raw)
            except ValueError:
                print(f"Invalid input. Please enter a number from {minimum} to {maximum}.")
                continue
            if minimum <= choice <= maximum:
                return choice
            print(f"Invalid choice. Please enter a number from {minimum} to {maximum}.")

    def get_yes_or_no(prompt):
        while True:
            ans = input(prompt).strip().lower()
            if ans in ("y", "yes"):  return True
            if ans in ("n", "no"):   return False
            print("Invalid input. Please enter Y or N.")

    def pause(message="Press Enter to continue..."):
        input(message)

try:
    from security.save_load import load_game
except ImportError:
    def load_game():
        print("  Load system not connected yet.")
        return None


# ── Display helpers ─────────────────────────────────────────────────────────

TITLE = r"""
  +==================================================+
  |                                                  |
  |        S E C T O R   8                          |
  |        A Text-Based Escape                       |
  |                                                  |
  +==================================================+
"""


def print_title():
    print("\n" + TITLE)
    print("  CYSE-130 Final Project | Spring 2026\n")


def print_menu():
    print()
    print("  +================================+")
    print("  |       SECTOR 8 ADVENTURE       |")
    print("  +================================+")
    print("  | 1. New Game                    |")
    print("  | 2. Load Game                   |")
    print("  | 3. How to Play                 |")
    print("  | 4. View Audit Log              |")
    print("  | 5. Credits                     |")
    print("  | 6. Quit                        |")
    print("  +================================+")


def show_credits():
    print()
    print("  SECTOR 8 - Text-Based Adventure Game")
    print("  CYSE-130 Final Project | Spring 2026\n")
    print("  DEVELOPMENT TEAM:")
    print("    Role 1 (Core Engine):       Abdulrahman, Rehan, Raki")
    print("    Role 2 (Story & NPCs):      Nithin, Nawaf")
    print("    Role 3 (Systems & Security): Sami, Bader\n")
    pause()


def show_how_to_play():
    print("\n  HOW TO PLAY")
    print("  -----------")
    print("  Choose numbered options to move through the story.")
    print("  Type M during a scene to open the action menu.")
    print("  The action menu lets you view inventory, use items,")
    print("  save the game, check your status, or quit.")
    print("  There are 3 story paths and 3 endings.")
    print("  Invalid input is rejected - the game will ask again.\n")
    log_event("MENU_VIEW", detail="How to Play", result="SUCCESS")
    pause()


def show_audit_log():
    if not os.path.exists(audit_log_path):
        print("\n  No audit log found yet.\n")
        return
    print("\n  ====== AUDIT LOG (last 30 entries) ======\n")
    try:
        with open(audit_log_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines[-30:]:
                print(f"  {line.rstrip()}")
    except OSError as e:
        print(f"  Error reading log: {e}")
    print()
    pause()


# ── Game loop ───────────────────────────────────────────────────────────────

def play_game(game_state):
    if not isinstance(game_state, dict):
        print("  Game could not start - invalid game_state.")
        log_event("ERROR", detail="play_game got invalid game_state", result="FAIL")
        return

    while True:
        scene_key = game_state.get("current_scene", "start")
        try:
            next_scene = run_scene(scene_key, game_state)
        except KeyboardInterrupt:
            print("\n  Game interrupted.")
            log_event("GAME_END", detail="KeyboardInterrupt", result="FAIL")
            return
        except Exception as error:
            print("\n  Unexpected error - returning to main menu.")
            log_event("ERROR", detail=f"Game loop error={error}", result="FAIL")
            return

        if next_scene is None:
            print("\n  Thanks for playing.")
            log_event("GAME_END", detail="Player quit during game", result="SUCCESS")
            return
        if next_scene == "end":
            print("\n  Game over. Returning to main menu.")
            log_event("GAME_END", detail="Player reached ending", result="SUCCESS")
            return

        if isinstance(next_scene, str) and next_scene.strip():
            game_state["current_scene"] = next_scene
        else:
            log_event("ERROR", detail=f"Invalid next_scene={next_scene}", result="FAIL")
            game_state["current_scene"] = "start"


def start_new_game():
    game_state = create_new_state()
    log_event("GAME_START", detail="New game", result="SUCCESS")
    return game_state


def start_loaded_game():
    gs = load_game()
    if gs is not None:
        print("\n  Save loaded successfully.")
        log_event("GAME_START", detail="Continued from save", result="SUCCESS")
        return gs
    print("\n  No valid save could be loaded.")
    if get_yes_or_no("  Start a new game instead? (Y/N): "):
        return start_new_game()
    log_event("LOAD_ATTEMPT", detail="Returned to menu after failed load", result="FAIL")
    return None


# ── Entry point ─────────────────────────────────────────────────────────────

def main():
    print_title()
    log_event("PROGRAM_START", detail="main.py started", result="SUCCESS")

    while True:
        print_menu()
        choice = get_valid_number("  Enter your choice (1-6): ", 1, 6)
        log_event("INPUT", detail=f"MainMenu choice={choice}", result="SUCCESS")

        if choice == 1:
            play_game(start_new_game())
        elif choice == 2:
            gs = start_loaded_game()
            if gs is not None:
                play_game(gs)
        elif choice == 3:
            show_how_to_play()
        elif choice == 4:
            show_audit_log()
        elif choice == 5:
            show_credits()
        elif choice == 6:
            log_event("GAME_END", detail="Quit from main menu", result="SUCCESS")
            print("\n  Thank you for playing Sector 8!\n")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  [Game interrupted]\n")
        log_event("PROGRAM_END", detail="Interrupted")
        sys.exit(0)
    except Exception as e:
        print(f"\n  [Error: {e}]\n")
        log_event("ERROR", detail=str(e))
        sys.exit(1)
