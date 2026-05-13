# systems/challenges.py
# Role 3 - Bader
# Challenge mini-games. run_challenge() is imported by engine/game_engine.py

try:
    from security.security import log_event
except ImportError:
    def log_event(event_type, detail="", result=""):
        pass


def _ensure_game_state(gs):
    if "flags"     not in gs: gs["flags"]     = {}
    if "inventory" not in gs: gs["inventory"] = []
    if "health"    not in gs: gs["health"]    = 100


def terminal_login_challenge(game_state):
    """Password puzzle. Correct = 2019MV (year + director initials)."""
    _ensure_game_state(game_state)
    print("\n  --- Terminal Login Challenge ---")
    print("  The terminal asks for a password.")
    print("  You have 3 attempts before the terminal locks.")
    print("  Hint: Use the facility year and the director's initials.")
    print("  Example format: 0000AB\n")

    correct = "2019mv"
    attempts_left = 3
    while attempts_left > 0:
        guess = input("  Enter password: ").strip().lower()
        if guess == correct:
            print("\n  ACCESS GRANTED.")
            print("  The terminal unlocks the security controls.\n")
            game_state["flags"]["terminal_hacked"] = True
            game_state["flags"]["alarm_disabled"] = True
            log_event("CHALLENGE_ATTEMPT", detail="Puzzle=terminal_login", result="SUCCESS")
            return True
        attempts_left -= 1
        print(f"\n  Incorrect password. Attempts left: {attempts_left}\n")
        log_event("CHALLENGE_ATTEMPT", detail=f"Puzzle=terminal_login Left={attempts_left}", result="FAIL")
    print("  The terminal locks you out.\n")
    return False


def guard_dog_challenge(game_state):
    """Guard dog. Auto-passes if player has Vending Snacks."""
    _ensure_game_state(game_state)
    print("\n  --- Guard Dog Challenge ---")
    print("  A guard dog blocks the maintenance tunnel.\n")

    if "Vending Snacks" in game_state["inventory"]:
        print("  You throw the vending snacks across the room.")
        print("  The dog runs after them, giving you time to escape.\n")
        game_state["inventory"].remove("Vending Snacks")
        log_event("CHALLENGE_ATTEMPT", detail="Puzzle=guard_dog Used=Vending Snacks", result="SUCCESS")
        return True

    while True:
        print("  What do you do?")
        print("  1. Try to sneak past the dog")
        print("  2. Run straight to the tunnel")
        print("  3. Back away slowly")
        choice = input("  Enter your choice (1-3): ").strip()

        if choice == "1":
            print("\n  The dog hears your footsteps and blocks your path.\n")
            log_event("CHALLENGE_ATTEMPT", detail="Puzzle=guard_dog Choice=sneak", result="FAIL")
            return False
        elif choice == "2":
            print("\n  The dog charges. You retreat and lose 20 HP.\n")
            game_state["health"] = max(0, game_state["health"] - 20)
            log_event("CHALLENGE_ATTEMPT", detail="Puzzle=guard_dog Choice=run", result="FAIL")
            return False
        elif choice == "3":
            print("\n  You back away safely. Find something to distract the dog.\n")
            log_event("CHALLENGE_ATTEMPT", detail="Puzzle=guard_dog Choice=back_away", result="FAIL")
            return False
        else:
            print("\n  Invalid choice. Please enter 1, 2, or 3.\n")
            log_event("INPUT_INVALID", detail=f"GuardDog bad='{choice}'", result="FAIL")


def drone_patrol_challenge(game_state):
    """Bonus challenge - security drone."""
    _ensure_game_state(game_state)
    print("\n  --- Security Drone Challenge ---")
    print("  A security drone patrols the hallway.\n")

    while True:
        print("  What do you do?")
        print("  1. Hide behind a metal crate")
        print("  2. Throw an object to distract it")
        print("  3. Run through the hallway")
        choice = input("  Enter your choice (1-3): ").strip()

        if choice == "1":
            print("\n  You hide. The drone passes. You continue safely.\n")
            log_event("CHALLENGE_ATTEMPT", detail="Puzzle=drone_patrol Choice=hide", result="SUCCESS")
            return True
        elif choice == "2":
            print("\n  The drone investigates the noise. You slip by.\n")
            log_event("CHALLENGE_ATTEMPT", detail="Puzzle=drone_patrol Choice=distract", result="SUCCESS")
            return True
        elif choice == "3":
            print("\n  Spotted! The alarm goes off. You lose 15 HP.\n")
            game_state["health"] = max(0, game_state["health"] - 15)
            log_event("CHALLENGE_ATTEMPT", detail="Puzzle=drone_patrol Choice=run", result="FAIL")
            return False
        else:
            print("\n  Invalid choice. Please enter 1, 2, or 3.\n")
            log_event("INPUT_INVALID", detail=f"DronePatrol bad='{choice}'", result="FAIL")


def run_challenge(challenge_key, game_state):
    """Main router - called by engine/game_engine.py"""
    _ensure_game_state(game_state)
    challenges = {
        "terminal_login": terminal_login_challenge,
        "guard_dog":      guard_dog_challenge,
        "drone_patrol":   drone_patrol_challenge,
    }
    fn = challenges.get(challenge_key)
    if fn is None:
        print(f"\n  [ERROR] Challenge '{challenge_key}' not found. Auto-failing.\n")
        log_event("ERROR", detail=f"Missing challenge='{challenge_key}'", result="FAIL")
        return False
    return fn(game_state)
