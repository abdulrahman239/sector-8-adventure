# content/story.py
# Role 2 - Story scenes and branching logic
# Each scene is a dictionary with text, choices, and conditions.

# ─────────────────────────────────────────────
# STORY FLAGS (track player decisions)
# ─────────────────────────────────────────────
# These are stored inside game_state["flags"] (dict of booleans).
# The engine (Role 1) passes game_state in; we read and write flags here.

def get_initial_flags():
    """Return the default starting flags for a new game."""
    return {
        "has_keycard": False,
        "terminal_hacked": False,
        "scientist_rescued": False,
        "alarm_disabled": False,
        "guard_bribed": False,
    }


# ─────────────────────────────────────────────
# SCENE DEFINITIONS
# ─────────────────────────────────────────────
# Each scene dict has:
#   "text"    : str  - narration shown to the player
#   "choices" : list of dicts, each with:
#       "label"     : str  - what the player sees (e.g. "1. Search for a keycard")
#       "next_scene": str  - key of the next scene to load
#       "condition" : callable(game_state) -> bool  (optional, defaults to True)
#       "effect"    : callable(game_state) -> None  (optional, runs on selection)

SCENES = {

    # ── BEGINNING (shared opening) ────────────────────────────────────────────
    "start": {
        "text": (
            "You wake up inside a locked research facility.\n"
            "Emergency lights flicker. An alarm loops in the distance.\n"
            "A sign on the wall reads: SECTOR 7 — AUTHORIZED PERSONNEL ONLY.\n\n"
            "Three paths stretch before you."
        ),
        "choices": [
            {
                "label": "1. Search the nearby offices for a keycard",
                "next_scene": "office_search",
            },
            {
                "label": "2. Head to the server room and hack the terminal",
                "next_scene": "server_room",
            },
            {
                "label": "3. Follow the voice crying for help down the east corridor",
                "next_scene": "east_corridor",
            },
        ],
    },

    # ── PATH 1: Find the Keycard ───────────────────────────────────────────────
    "office_search": {
        "text": (
            "You slip into a row of dark offices.\n"
            "Desks are overturned. A guard's radio crackles on the floor.\n"
            "Guard Chen steps out from the shadows, hand on her taser."
        ),
        "choices": [
            {
                "label": "1. Try to bribe Guard Chen with the vending machine snacks",
                "next_scene": "bribe_guard",
                "condition": lambda gs: "Vending Snacks" in gs["inventory"],
                "effect": lambda gs: gs["flags"].update({"guard_bribed": True}),
            },
            {
                "label": "2. Distract her by triggering a fire alarm in the side hall",
                "next_scene": "distract_guard",
            },
            {
                "label": "3. Ask Chen for help — explain what happened",
                "next_scene": "talk_to_chen",
            },
        ],
    },

    "bribe_guard": {
        "text": (
            "Chen raises an eyebrow, then pockets the chips.\n"
            "'There's a keycard in the top-left drawer. Don't tell anyone.'\n"
            "She turns and walks away. You grab the keycard."
        ),
        "choices": [
            {
                "label": "1. Head to the loading bay exit",
                "next_scene": "loading_bay",
                "effect": lambda gs: (
                    gs["flags"].update({"has_keycard": True}),
                    gs["inventory"].append("Keycard") if "Keycard" not in gs["inventory"] else None,
                ),
            },
        ],
    },

    "distract_guard": {
        "text": (
            "The fire alarm screams. Chen bolts toward the side hall.\n"
            "You have 90 seconds. You tear through the desk drawers\n"
            "and find a keycard taped underneath the last one."
        ),
        "choices": [
            {
                "label": "1. Run to the loading bay before she returns",
                "next_scene": "loading_bay",
                "effect": lambda gs: (
                    gs["flags"].update({"has_keycard": True}),
                    gs["inventory"].append("Keycard") if "Keycard" not in gs["inventory"] else None,
                ),
            },
        ],
    },

    "talk_to_chen": {
        "text": (
            "Chen listens, expression softening.\n"
            "'I heard the explosion in Lab C. Here — take my keycard.\n"
            "Loading bay is your best shot. Go.'\n"
            "She presses the keycard into your hand."
        ),
        "choices": [
            {
                "label": "1. Thank her and head to the loading bay",
                "next_scene": "loading_bay",
                "effect": lambda gs: (
                    gs["flags"].update({"has_keycard": True}),
                    gs["inventory"].append("Keycard") if "Keycard" not in gs["inventory"] else None,
                ),
            },
        ],
    },

    "loading_bay": {
        "text": (
            "The loading bay door has a card reader.\n"
            "Beyond the steel door you can hear rain — and freedom."
        ),
        "choices": [
            {
                "label": "1. Swipe the keycard",
                "next_scene": "ending_loading_bay",
                "condition": lambda gs: gs["flags"].get("has_keycard"),
            },
            {
                "label": "1. [You need a keycard to open this door]",
                "next_scene": "loading_bay",
                "condition": lambda gs: not gs["flags"].get("has_keycard"),
            },
        ],
    },

    # ── PATH 2: Hack the Terminal ─────────────────────────────────────────────
    "server_room": {
        "text": (
            "Banks of humming servers surround you in cold blue light.\n"
            "A terminal glows in the center of the room.\n"
            "LOGIN REQUIRED — 3 attempts before lockout."
        ),
        "choices": [
            {
                "label": "1. Try to crack the terminal password",
                "next_scene": "terminal_puzzle",
            },
            {
                "label": "2. Look around the server room for clues",
                "next_scene": "server_room_clue",
            },
        ],
    },

    "server_room_clue": {
        "text": (
            "A sticky note on the back of monitor 3 reads:\n"
            "'Password reminder: year the facility opened + director's initials'\n"
            "A nameplate on the wall says: Director M. Vasquez, Est. 2019.\n"
        ),
        "choices": [
            {
                "label": "1. Return to the terminal and try the password",
                "next_scene": "terminal_puzzle",
            },
        ],
    },

    "terminal_puzzle": {
        # NOTE: The actual puzzle challenge logic lives in systems/challenges.py (Role 3).
        # This scene hands off to the challenge runner and then routes based on result.
        "text": "You sit down at the terminal. The cursor blinks.",
        "choices": [
            {
                "label": "1. Attempt to log in  [PUZZLE]",
                "next_scene": "terminal_success",   # engine checks challenge result
                "challenge": "terminal_login",       # Role 1 engine resolves this
            },
        ],
    },

    "terminal_success": {
        "text": (
            "ACCESS GRANTED.\n"
            "You pull up the facility map, disable the east alarm zone,\n"
            "and unlock the security checkpoint door."
        ),
        "choices": [
            {
                "label": "1. Head to the security checkpoint",
                "next_scene": "ending_checkpoint",
                "effect": lambda gs: gs["flags"].update({
                    "terminal_hacked": True,
                    "alarm_disabled": True,
                }),
            },
        ],
    },

    # ── PATH 3: Help the Scientist ────────────────────────────────────────────
    "east_corridor": {
        "text": (
            "The crying grows louder. Behind a collapsed shelf\n"
            "you find Dr. Reyes, pinned but alive.\n"
            "'Please — help me. I know another way out.'"
        ),
        "choices": [
            {
                "label": "1. Lift the shelf and free Dr. Reyes",
                "next_scene": "rescue_scientist",
            },
            {
                "label": "2. Leave her and find your own way out",
                "next_scene": "leave_scientist",
            },
        ],
    },

    "rescue_scientist": {
        "text": (
            "You heave the shelf aside. Dr. Reyes gasps, stands.\n"
            "'Thank you. Take this — access code 7-7-DELTA. And this emergency badge.\n"
            "The maintenance tunnel is behind Lab C. But... there's a guard dog.'"
        ),
        "choices": [
            {
                "label": "1. Head to the maintenance tunnel",
                "next_scene": "maintenance_encounter",
                "effect": lambda gs: (
                    gs["flags"].update({"scientist_rescued": True}),
                    gs["inventory"].append("Emergency Badge") if "Emergency Badge" not in gs["inventory"] else None,
                    gs["inventory"].append("Access Code: 7-7-DELTA") if "Access Code: 7-7-DELTA" not in gs["inventory"] else None,
                ),
            },
        ],
    },

    "leave_scientist": {
        "text": (
            "Her cries fade behind you.\n"
            "The east corridor dead-ends at a locked maintenance door.\n"
            "You don't have the code."
        ),
        "choices": [
            {
                "label": "1. Go back and help Dr. Reyes after all",
                "next_scene": "rescue_scientist",
            },
            {
                "label": "2. Turn around and try a different path",
                "next_scene": "start",
            },
        ],
    },

    "maintenance_encounter": {
        "text": (
            "Lab C. A heavy door. On the other side — growling.\n"
            "The guard dog. You need to get past it."
        ),
        "choices": [
            {
                "label": "1. Use the vending snacks to distract the dog",
                "next_scene": "ending_maintenance",
                "condition": lambda gs: "Vending Snacks" in gs["inventory"],
                "challenge": "guard_dog",
            },
            {
                "label": "1. [You need something to distract the dog]",
                "next_scene": "maintenance_stuck",
                "condition": lambda gs: "Vending Snacks" not in gs["inventory"],
            },
        ],
    },

    "maintenance_stuck": {
        "text": (
            "The dog snarls. You back away.\n"
            "You need a distraction — something the dog would want."
        ),
        "choices": [
            {
                "label": "1. Go look for something in the vending machine area",
                "next_scene": "vending_machine",
            },
        ],
    },

    "vending_machine": {
        "text": (
            "A cracked vending machine in the break room still has snacks.\n"
            "You pry open the panel and grab a bag of chips.\n"
            "There's also a wall-mounted first aid box. You take the kit inside."
        ),
        "choices": [
            {
                "label": "1. Head back to Lab C",
                "next_scene": "maintenance_encounter",
                "effect": lambda gs: (
                    gs["inventory"].append("Vending Snacks") if "Vending Snacks" not in gs["inventory"] else None,
                    gs["inventory"].append("First Aid Kit") if "First Aid Kit" not in gs["inventory"] else None,
                ),
            },
        ],
    },

    # ── ENDINGS ───────────────────────────────────────────────────────────────
    "ending_loading_bay": {
        "text": (
            "The door clicks open. Rain hits your face.\n"
            "You sprint across the loading dock into the dark.\n\n"
            "╔══════════════════════════════╗\n"
            "║  ENDING 1 — The Clean Escape ║\n"
            "╚══════════════════════════════╝\n"
            "You escaped with Guard Chen's help. She later filed a report\n"
            "claiming the keycard was 'lost in the emergency.' Smart."
        ),
        "choices": [],  # empty = game over, engine handles restart prompt
        "ending": "loading_bay_escape",
    },

    "ending_checkpoint": {
        "text": (
            "The checkpoint door slides open. Two confused guards wave you through.\n"
            "The system shows your clearance as DIRECTOR-LEVEL. They don't argue.\n\n"
            "╔═══════════════════════════════════╗\n"
            "║  ENDING 2 — The Ghost in the Wire ║\n"
            "╚═══════════════════════════════════╝\n"
            "You hacked your way out. The breach was never officially reported.\n"
            "Someone deleted the logs."
        ),
        "choices": [],
        "ending": "checkpoint_escape",
    },

    "ending_maintenance": {
        "text": (
            "The dog happily destroys the chips. You slip through Lab C\n"
            "and sprint down the maintenance tunnel into the cold night air.\n\n"
            "╔══════════════════════════════════╗\n"
            "║  ENDING 3 — The Tunnel at Dawn   ║\n"
            "╚══════════════════════════════════╝\n"
            "You and Dr. Reyes escaped together. She still owes you one."
        ),
        "choices": [],
        "ending": "maintenance_escape",
    },
}


# ─────────────────────────────────────────────
# PUBLIC FUNCTIONS (called by the engine)
# ─────────────────────────────────────────────

def get_scene(scene_key):
    """
    Return the scene dict for scene_key.
    Raises KeyError if the scene doesn't exist (engine should handle this).
    """
    if scene_key not in SCENES:
        raise KeyError(f"Scene '{scene_key}' not found in SCENES.")
    return SCENES[scene_key]


def get_available_choices(scene, game_state):
    """
    Filter a scene's choices by their condition (if any).
    Returns a list of choices the player can currently select.

    Example usage in engine:
        scene = get_scene(current_scene_key)
        choices = get_available_choices(scene, game_state)
    """
    available = []
    for choice in scene["choices"]:
        condition = choice.get("condition")
        if condition is None or condition(game_state):
            available.append(choice)
    return available


def apply_choice_effect(choice, game_state):
    """
    Run the effect function of a chosen option (if it has one).
    Call this after the player selects a valid choice.
    """
    effect = choice.get("effect")
    if effect:
        effect(game_state)


def is_ending(scene):
    """Return True if this scene is a game-ending scene."""
    return "ending" in scene and len(scene["choices"]) == 0
