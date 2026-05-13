# systems/inventory.py
# Role 2 - Inventory system
# Manages the player's item collection, viewing, and usage.

# ─────────────────────────────────────────────

# ─────────────────────────────────────────────
# USE EFFECT FUNCTIONS
# ─────────────────────────────────────────────

def _use_keycard(game_state):
    if game_state["current_scene"] == "loading_bay":
        game_state["flags"]["has_keycard"] = True
        return "You swipe the keycard. The reader flashes green. The door clicks open."
    return "You hold up the keycard. There's nothing to use it on here."


def _use_badge(game_state):
    game_state["flags"]["badge_used"] = True
    return (
        "You flash the emergency badge at the scanner.\n"
        "A light blinks. The system registers EMERGENCY CLEARANCE — LEVEL 2."
    )


def _use_access_code(game_state):
    if game_state["current_scene"] in ("maintenance_encounter", "maintenance_stuck"):
        game_state["flags"]["tunnel_code_used"] = True
        return (
            "You punch in 7-7-DELTA on the keypad.\n"
            "The maintenance door grinds open."
        )
    return "You read the code to yourself. You'll need to find the right keypad."


def _use_snacks(game_state):
    game_state["flags"]["dog_distracted"] = True
    return (
        "You toss the chips across the room.\n"
        "The guard dog lunges for them without a second glance at you."
    )


def _use_first_aid(game_state):
    healed = min(30, 100 - game_state.get("health", 100))
    game_state["health"] = game_state.get("health", 100) + healed
    return f"You patch yourself up. +{healed} HP. (Health: {game_state['health']}/100)"


# ─────────────────────────────────────────────
# INVENTORY FUNCTIONS (called by the engine)
# ─────────────────────────────────────────────

def add_item(inventory, item_name):
    """
    Add item_name to the inventory list.
    Prevents duplicates for non-stackable items.
    Returns a result message string.
    """
    if item_name not in ITEMS:
        return f"Unknown item: '{item_name}'"
    if item_name in inventory:
        return f"You already have: {item_name}"
    inventory.append(item_name)
    return f"[Item added: {item_name}]"


def remove_item(inventory, item_name):
    """
    Remove item_name from the inventory list.
    Returns a result message string.
    """
    if item_name not in inventory:
        return f"You don't have: {item_name}"
    inventory.remove(item_name)
    return f"[Item removed: {item_name}]"


def use_item(inventory, item_name, game_state):
    """
    Use an item from inventory.
    Applies the item's effect and removes it if consumable.
    Returns result text to display to the player.

    Example usage in engine:
        result = use_item(game_state["inventory"], "First Aid Kit", game_state)
        print(result)
    """
    if item_name not in inventory:
        return f"You don't have '{item_name}' in your inventory."

    if item_name not in ITEMS:
        return f"'{item_name}' has no defined use."

    item = ITEMS[item_name]
    result = item["use_effect"](game_state)

    if item["consumable"] and item_name in inventory:
        inventory.remove(item_name)
        result += f"\n[{item_name} was used up]"

    return result


def show_inventory(inventory):
    """
    Return a formatted string listing the player's current inventory.
    Call this whenever the player chooses 'View Inventory'.
    """
    if not inventory:
        return "Your inventory is empty."

    lines = ["── Inventory ──────────────────────"]
    for i, item_name in enumerate(inventory, start=1):
        desc = ITEMS.get(item_name, {}).get("description", "No description available.")
        lines.append(f"  {i}. {item_name}")
        lines.append(f"     {desc}")
    lines.append("────────────────────────────────")
    return "\n".join(lines)


def get_item_names():
    """Return a list of all possible item names in the game."""
    return list(ITEMS.keys())

# ITEM DEFINITIONS
# ─────────────────────────────────────────────
# Each item has a description and a use_effect.
# use_effect(game_state) -> str: applies the item's effect, returns result text.
# consumable: if True, item is removed from inventory after use.

ITEMS = {
    "Keycard": {
        "description": "A standard facility access card. Unlocks the loading bay exit.",
        "consumable": False,
        "use_effect": _use_keycard,
    },
    "Emergency Badge": {
        "description": "Dr. Reyes' emergency clearance badge. Grants limited access.",
        "consumable": False,
        "use_effect": _use_badge,
    },
    "Access Code: 7-7-DELTA": {
        "description": "A handwritten tunnel access code from Dr. Reyes.",
        "consumable": False,
        "use_effect": _use_access_code,
    },
    "Vending Snacks": {
        "description": "A bag of BBQ chips. Dogs love these.",
        "consumable": True,
        "use_effect": _use_snacks,
    },
    "First Aid Kit": {
        "description": "A basic med kit found in the break room. Restores 30 HP.",
        "consumable": True,
        "use_effect": _use_first_aid,
    },
}
