# engine/game_engine.py
# Role 1 - Abdulrahman
# Core game engine.

import sys

from content.story     import get_scene, get_available_choices, apply_choice_effect, is_ending
from content.npcs      import get_npcs_in_scene, run_npc_interaction, get_npc
from systems.inventory import show_inventory, use_item

try:
    from systems.challenges import run_challenge
except ImportError:
    def run_challenge(challenge_key, game_state):
        print("\n  [Challenge system not connected yet - auto-passing]\n")
        return True

try:
    from security.security import log_event
except ImportError:
    def log_event(event_type, detail="", result=""):
        pass

try:
    from security.save_load import save_game
except ImportError:
    def save_game(game_state):
        print("\n  [Save system not connected yet]\n")


def _divider(char="=", width=52):
    print("\n" + char * width)

def _print_scene(scene):
    _divider("=")
    print()
    print(scene["text"])
    print()
    _divider("=")

def _print_choices(choices):
    print()
    for choice in choices:
        print(f"  {choice['label']}")
    print()
    print("  M  -  Open Menu  (inventory / use item / save / status / quit)")
    print()

def _action_menu(game_state):
    while True:
        print()
        print("  +==============================+")
        print("  |        ACTION MENU           |")
        print("  +==============================+")
        print("  |  1. View Inventory            |")
        print("  |  2. Use an Item               |")
        print("  |  3. Save Game                 |")
        print("  |  4. Player Status             |")
        print("  |  5. Back to Game              |")
        print("  |  6. Quit Game                 |")
        print("  +==============================+")
        print()
        raw = input("  Enter a number (1-6): ").strip()
        log_event("INPUT", detail=f"ActionMenu input='{raw}'")
        try:
            choice = int(raw)
        except ValueError:
            log_event("INPUT_INVALID", detail=f"ActionMenu non-integer='{raw}'")
            print("\n  Invalid input. Please enter a number from 1 to 6.\n")
            continue
        if choice == 1:
            print()
            print(show_inventory(game_state["inventory"]))
        elif choice == 2:
            _use_item_menu(game_state)
        elif choice == 3:
            save_game(game_state)
            log_event("SAVE_ATTEMPT", result="SUCCESS")
            print("\n  Game saved.\n")
        elif choice == 4:
            try:
                from engine.state import summary
                print()
                print(summary(game_state))
                print()
            except ImportError:
                print(f"\n  Health : {game_state.get('health', 100)}/100")
                print(f"  Scene  : {game_state.get('current_scene', '?')}")
                inv = game_state.get("inventory", [])
                print(f"  Items  : {', '.join(inv) if inv else '(empty)'}\n")
        elif choice == 5:
            return False
        elif choice == 6:
            confirm = input("\n  Are you sure you want to quit? (Y/N): ").strip().upper()
            if confirm == "Y":
                log_event("GAME_END", detail="Player quit from action menu")
                return True
            else:
                print("\n  Returning to menu.\n")
        else:
            log_event("INPUT_INVALID", detail=f"ActionMenu out-of-range='{raw}'")
            print("\n  Invalid choice. Please enter a number from 1 to 6.\n")

def _use_item_menu(game_state):
    items = game_state["inventory"]
    if not items:
        print("\n  Your inventory is empty. Nothing to use.\n")
        return
    print()
    for i, name in enumerate(items, 1):
        print(f"    {i}. {name}")
    print("    0. Cancel")
    print()
    raw = input("  Enter item number to use: ").strip()
    try:
        idx = int(raw)
    except ValueError:
        log_event("INPUT_INVALID", detail=f"UseItem non-integer='{raw}'")
        print("\n  Invalid input. Returning to menu.\n")
        return
    if idx == 0:
        return
    if 1 <= idx <= len(items):
        item_name = items[idx - 1]
        result = use_item(game_state["inventory"], item_name, game_state)
        print(f"\n  {result}\n")
        log_event("ITEM_USED", detail=f"Item={item_name}")
    else:
        print("\n  No item with that number.\n")

def _npc_menu(scene_key, game_state):
    npcs_here = get_npcs_in_scene(scene_key)
    if not npcs_here:
        return
    print()
    print("  -- People nearby --")
    for i, npc_key in enumerate(npcs_here, 1):
        npc = get_npc(npc_key)
        print(f"  T{i}. {npc['name']}")
        print(f"      {npc['description']}")
    print("  T0. Skip")
    print()
    raw = input(f"  Talk to someone? Enter T0-T{len(npcs_here)}: ").strip().upper()
    log_event("INPUT", detail=f"NPCMenu scene={scene_key} input='{raw}'")
    if raw in ("T0", "0"):
        return
    try:
        idx = int(raw.replace("T", "")) - 1
    except ValueError:
        log_event("INPUT_INVALID", detail=f"NPCMenu bad input='{raw}'")
        print("\n  Invalid input - skipping.\n")
        return
    if 0 <= idx < len(npcs_here):
        npc_key = npcs_here[idx]
        npc = get_npc(npc_key)
        print()
        print(f"  -- {npc['name']} --")
        print()
        print(run_npc_interaction(npc_key, game_state))
        print()
        log_event("NPC_INTERACTION", detail=f"NPC={npc_key} scene={scene_key}")
    else:
        print("\n  No one with that number.\n")

def _get_player_choice(choices, scene_key, game_state):
    n = len(choices)
    while True:
        _print_choices(choices)
        raw = input(f"  Enter your choice (1-{n}): ").strip().upper()
        log_event("INPUT", detail=f"Scene={scene_key} input='{raw}'")
        if raw == "M":
            quit_requested = _action_menu(game_state)
            if quit_requested:
                return None
            continue
        try:
            idx = int(raw) - 1
        except ValueError:
            log_event("INPUT_INVALID", detail=f"Scene={scene_key} non-integer='{raw}'")
            print(f"\n  Invalid input. Please enter a number from 1 to {n}, or M for Menu.\n")
            continue
        if 0 <= idx < n:
            selected = choices[idx]
            log_event("CHOICE_MADE", detail=f"Scene={scene_key} Choice='{selected['label'][:50]}'")
            return selected
        else:
            log_event("INPUT_INVALID", detail=f"Scene={scene_key} out-of-range='{raw}'")
            print(f"\n  Invalid choice. Please enter a number from 1 to {n}.\n")

def _handle_challenge(choice, game_state):
    challenge_key = choice.get("challenge")
    if not challenge_key:
        return True
    print()
    print(f"  -- CHALLENGE: {challenge_key} --")
    log_event("CHALLENGE_ATTEMPT", detail=f"Puzzle={challenge_key}", result="START")
    passed = run_challenge(challenge_key, game_state)
    result_str = "SUCCESS" if passed else "FAIL"
    log_event("CHALLENGE_ATTEMPT", detail=f"Puzzle={challenge_key}", result=result_str)
    return passed

def run_scene(scene_key, game_state):
    try:
        scene = get_scene(scene_key)
    except KeyError:
        print(f"\n  [ERROR] Scene '{scene_key}' not found. Returning to start.\n")
        log_event("ERROR", detail=f"Missing scene key='{scene_key}'")
        return "start"
    _print_scene(scene)
    _npc_menu(scene_key, game_state)
    if is_ending(scene):
        log_event("GAME_END", detail=f"Ending={scene.get('ending', scene_key)}")
        input("\n  Press Enter to continue...\n")
        return "end"
    available = get_available_choices(scene, game_state)
    if not available:
        print("\n  [No available choices - returning to start]\n")
        log_event("ERROR", detail=f"No available choices at scene='{scene_key}'")
        return "start"
    selected = _get_player_choice(available, scene_key, game_state)
    if selected is None:
        return None
    if not _handle_challenge(selected, game_state):
        print("\n  Challenge failed. Try again.\n")
        return scene_key
    apply_choice_effect(selected, game_state)
    return selected["next_scene"]
