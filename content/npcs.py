# content/npcs.py
# Role 2 - NPC definitions and interaction logic
# Each NPC has dialogue and a run_interaction() function.

# ─────────────────────────────────────────────
# NPC REGISTRY
# ─────────────────────────────────────────────
# Each NPC dict contains:
#   "name"        : str
#   "location"    : str  (scene key where they appear)
#   "description" : str  (shown when player first meets them)
#   "interaction" : callable(game_state) -> str
#                   Runs when the player talks to / encounters the NPC.
#                   May modify game_state (flags, inventory).
#                   Returns dialogue/outcome text.


# ─────────────────────────────────────────────
# NPC INTERACTION FUNCTIONS
# ─────────────────────────────────────────────
# Each function receives game_state (dict) and may:
#   - Add items to game_state["inventory"]
#   - Set flags in game_state["flags"]
#   - Return multi-line dialogue strings

def _interact_chen(game_state):
    """
    Guard Chen — gives a clue about the keycard location.
    If the player has already bribed her, she gives a different response.
    """
    if game_state["flags"].get("guard_bribed"):
        return (
            "Chen glances at you and looks away.\n"
            "'You didn't see me. I didn't see you. Move.'"
        )

    return (
        "Chen crosses her arms.\n"
        "'I've worked here six years. Never seen anything like this.\n"
        " Look — I can't let you leave without authorization, but...\n"
        " the emergency keycard locker is in the east office. Third drawer.\n"
        " Technically I didn't tell you that.'\n\n"
        "[Clue obtained: keycard may be in the east office, third drawer]"
    )


def _interact_reyes(game_state):
    """
    Dr. Reyes — gives access code and badge if rescued, nothing if already helped.
    """
    if game_state["flags"].get("scientist_rescued"):
        return (
            "Dr. Reyes steadies herself against the wall.\n"
            "'I'm okay. The tunnel is just past Lab C.\n"
            " Watch out for the dog — it responds to food, not commands.'"
        )

    # First interaction — rescue and reward
    game_state["flags"]["scientist_rescued"] = True
    if "Emergency Badge" not in game_state["inventory"]:
        game_state["inventory"].append("Emergency Badge")
    if "Access Code: 7-7-DELTA" not in game_state["inventory"]:
        game_state["inventory"].append("Access Code: 7-7-DELTA")

    return (
        "You heave the shelf aside. Dr. Reyes gasps with relief.\n"
        "'You saved my life. Here — take my badge and the tunnel code.\n"
        " 7-7-DELTA. There's a maintenance exit behind Lab C.\n"
        " There's a guard dog. It's hungry. Find something to distract it.'\n\n"
        "[Item added: Emergency Badge]\n"
        "[Item added: Access Code: 7-7-DELTA]"
    )


def _interact_ko(game_state):
    """
    Janitor Ko — gives vending machine snacks and hints about the dog.
    Unique interaction: he knows more than he lets on.
    """
    if "Vending Snacks" in game_state["inventory"]:
        return (
            "Ko mops the floor without looking up.\n"
            "'You already got the chips. Don't waste them on yourself.'"
        )

    game_state["inventory"].append("Vending Snacks")

    return (
        "Ko looks at you with calm eyes.\n"
        "'Every alarm in this building goes off twice a year for drills.\n"
        " I don't worry anymore. Here — take these before the machine dies.\n"
        " That dog near Lab C loves the BBQ flavor.'\n"
        "He presses a bag of chips into your hand and keeps mopping.\n\n"
        "[Item added: Vending Snacks]"
    )


def _interact_aria(game_state):
    """
    ARIA — the facility AI. Gives a clue about the terminal password
    if the player asks. Won't unlock doors directly.
    """
    if game_state["flags"].get("terminal_hacked"):
        return (
            "ARIA: 'Access privileges confirmed. Please proceed to the designated exit.\n"
            " Have a productive day.'"
        )

    return (
        "ARIA: 'Hello. I am ARIA — Automated Research Intelligence Assistant.\n"
        " I am unable to unlock facility exits without proper authorization.\n"
        " However, I can confirm that our system passwords follow the format:\n"
        " [YEAR_ESTABLISHED][DIRECTOR_INITIALS].\n"
        " This information is publicly available on our website. Good luck.'\n\n"
        "[Clue obtained: password format = year + director initials]"
    )


def _interact_radio(game_state):
    """
    Unknown Radio Contact — triggers an optional story beat.
    Hints that someone on the outside is watching.
    Changes a flag that could influence which ending text is shown.
    """
    game_state["flags"]["radio_contacted"] = True

    return (
        "Static. Then a voice:\n"
        "'If you're hearing this, you're still inside. Good.\n"
        " Don't use the main exit — they're watching it.\n"
        " Loading bay or the maintenance tunnel. Your choice.\n"
        " And... don't trust the logs. Someone's been editing them.'\n"
        "The channel goes silent.\n\n"
        "[Flag set: radio_contacted — may affect ending dialogue]"
    )


# ─────────────────────────────────────────────
# PUBLIC FUNCTIONS (called by the engine)
# ─────────────────────────────────────────────

def get_npc(npc_key):
    """Return the NPC dict for npc_key."""
    if npc_key not in NPCS:
        raise KeyError(f"NPC '{npc_key}' not found.")
    return NPCS[npc_key]


def run_npc_interaction(npc_key, game_state):
    """
    Run the interaction function for an NPC.
    Returns the dialogue/outcome string to display to the player.

    Example usage in engine:
        result = run_npc_interaction("guard_chen", game_state)
        print(result)
    """
    npc = get_npc(npc_key)
    return npc["interaction"](game_state)


def get_npcs_in_scene(scene_key):
    """
    Return a list of NPC keys present in a given scene.
    Useful for the engine to know which NPCs to offer as interaction options.
    """
    return [key for key, npc in NPCS.items() if npc["location"] == scene_key]


NPCS = {

    "guard_chen": {
        "name": "Guard Chen",
        "location": "office_search",
        "description": "A tall security guard with a measured expression and a taser at her hip.",
        "interaction": _interact_chen,
    },

    "dr_reyes": {
        "name": "Dr. Reyes",
        "location": "east_corridor",
        "description": "A researcher in a torn lab coat, pinned under a collapsed shelf.",
        "interaction": _interact_reyes,
    },

    "janitor_ko": {
        "name": "Janitor Ko",
        "location": "vending_machine",
        "description": "An older man in coveralls who seems completely unbothered by the emergency.",
        "interaction": _interact_ko,
    },

    "ai_terminal": {
        "name": "ARIA (Automated Research Intelligence Assistant)",
        "location": "server_room",
        "description": "A synthetic voice coming from the server room terminal.",
        "interaction": _interact_aria,
    },

    "radio_voice": {
        "name": "Unknown Radio Contact",
        "location": "loading_bay",
        "description": "A crackling voice on an abandoned walkie-talkie near the loading dock.",
        "interaction": _interact_radio,
    },
}
