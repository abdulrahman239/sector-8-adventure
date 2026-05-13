# engine/state.py
# Role 1 - Rehan
# Game state initialization and management.

from content.story import get_initial_flags


def create_new_state():
    """
    Build and return a fresh game_state dict for a new game.
    This is the function imported by main.py.
    """
    # Start with the story's required flags, then add Rehan's tracking flags
    flags = get_initial_flags()
    flags.update({
        "path_keycard":         False,
        "path_hack":            False,
        "path_scientist":       False,
        "has_emergency_badge":  False,
        "has_access_code":      False,
        "has_vending_snacks":   False,
        "has_first_aid_kit":    False,
        "met_guard_chen":       False,
        "met_dr_reyes":         False,
        "met_janitor_ko":       False,
        "met_aria":             False,
        "met_radio_voice":      False,
        "dog_distracted":       False,
    })

    return {
        "current_scene": "start",
        "health":        100,
        "max_health":    100,
        "inventory":     [],
        "path_chosen":   None,
        "flags":         flags,
    }


# Alias so older code calling create_initial_state() still works
create_initial_state = create_new_state


def summary(game_state):
    """
    Return a readable status string for the player status screen.
    Called by game_engine.py action menu option 4.
    """
    inv = game_state["inventory"] if game_state["inventory"] else ["(empty)"]
    flags_on = [k for k, v in game_state["flags"].items() if v]
    return (
        f"  Scene   : {game_state['current_scene']}\n"
        f"  Health  : {game_state['health']}/{game_state.get('max_health', 100)}\n"
        f"  Items   : {', '.join(inv)}\n"
        f"  Flags   : {', '.join(flags_on) if flags_on else 'none'}"
    )


def is_alive(game_state):
    return game_state.get("health", 0) > 0


def set_scene(game_state, scene_key):
    game_state["current_scene"] = scene_key


def get_flag(game_state, flag_name, default=False):
    return game_state["flags"].get(flag_name, default)


def set_flag(game_state, flag_name, value=True):
    game_state["flags"][flag_name] = value
