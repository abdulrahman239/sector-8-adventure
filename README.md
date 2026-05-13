# Sector 8 — Text-Based Adventure Game
CYSE-130 Final Project | Spring 2026 | Group 8

## Team Members
| Name | Role | GitHub |
|------|------|--------|
| Abdulrahman | Core Engine + Integration | abdulrahman239 |
| Rehan Mohammed | Core Engine + Integration | Rehanm-7 |
| Raki Vijayakumar | Core Engine + Integration | dmvraki-ship-it |
| Nithin Arvind | Story + Gameplay Systems | NithinArv |
| Nawaf Alqahtani | Story + Gameplay Systems | n91ql |
| Sami Alwattar | Challenges + Cybersecurity | Sami42066 |
| Bader Alansari | Challenges + Cybersecurity | BQQ8 |

---

## How to Run the Game
1. Make sure Python 3 is installed
2. Download or clone this repository
3. Open a terminal in the project folder
4. Run: `python main.py`
5. From the main menu, choose `1. New Game` to begin

No external libraries are required — the game uses only the Python standard library.

---

## Core Game Features Included
- **Three branching story paths** with distinct routes, choices, and obstacles
- **Three different endings** based on which path the player follows
- **Six interactive locations** (1 starting + 5 path-specific scenes)
- **Five NPCs** with meaningful interactions (clues, items, choice triggers)
- **Inventory system** with five collectible items, viewable and usable at any time
- **Two challenges** — a password puzzle and an obstacle encounter, both with success/failure outcomes
- **Action menu** accessible mid-game via the `M` key (inventory, use item, save, status, quit)
- **Full Cyber Pack** — input validation, audit logging, and SHA-256 save tamper detection
- **Safe input handling** — the game never crashes on bad input; players are always re-prompted

---

## Story Paths and Endings

### The Three Story Paths
1. **Path 1 — Find the Keycard:** The player searches the offices, meets Guard Chen, and recovers a keycard either by bribing her with snacks, distracting her with a fire alarm, or asking her directly for help. They escape through the loading bay.
2. **Path 2 — Hack the Terminal:** The player heads to the server room, gathers password clues from a sticky note and the AI assistant ARIA, then solves the terminal login puzzle to disable alarms and unlock the security checkpoint exit.
3. **Path 3 — Help the Scientist:** The player follows cries for help to the east corridor, rescues Dr. Reyes, and receives her Emergency Badge and tunnel access code. After picking up snacks at the vending machine, they distract the guard dog at Lab C and escape through the maintenance tunnel.

### The Three Endings
1. **Ending 1 — The Clean Escape:** The player escapes through the loading bay using the keycard. Guard Chen covers for them in her after-action report.
2. **Ending 2 — The Ghost in the Wire:** The player escapes through the security checkpoint after hacking the terminal. The system reports them as having director-level clearance and the breach is never officially logged.
3. **Ending 3 — The Tunnel at Dawn:** The player and Dr. Reyes escape together through the maintenance tunnel after distracting the guard dog with vending snacks.

---

## Locations / Major Events
1. **Sector 8 Lobby (Start)** — The player wakes up locked inside the facility with three possible directions to take. This is the branching point that determines which path the player follows.
2. **Office Search** — The player encounters Guard Chen and must decide how to handle her (bribe, distract, or talk). This is a major event because the outcome determines whether the player obtains the Keycard.
3. **Server Room** — The player can attempt the terminal password challenge, with ARIA giving a clue about the password format. Picking the right clue sequence unlocks ending 2.
4. **East Corridor** — The player finds Dr. Reyes trapped and must decide whether to rescue her or leave her. Rescuing her grants two required items and unlocks path 3.
5. **Vending Machine / Break Room** — A pickup location where the player obtains Vending Snacks (required for the guard dog) and a First Aid Kit. Without visiting this location the guard dog challenge cannot be cleared.
6. **Lab C / Maintenance Tunnel** — The site of the guard dog challenge. Success leads to ending 3 through the maintenance tunnel.

---

## NPCs

| NPC | Where They Appear | What They Do |
|-----|-------------------|--------------|
| **Guard Chen** | Office Search | Gives a clue about the emergency keycard location. Reacts differently depending on whether the player bribes her with snacks, distracts her with a fire alarm, or asks her directly for help. Triggers the keycard pickup in all three sub-paths. |
| **Dr. Reyes** | East Corridor | When rescued, gives the player two key items (Emergency Badge and Access Code 7-7-DELTA) and warns about the guard dog at Lab C. Triggers the maintenance tunnel path. |
| **Janitor Ko** | Vending Machine | Provides optional dialogue and hints that the guard dog is hungry and loves BBQ-flavored snacks. Adds context to the Vending Snacks pickup. |
| **ARIA (Facility AI)** | Server Room | Provides a critical clue about the password format ("year established + director initials"). Without this clue, the terminal login challenge is much harder. |
| **Radio Voice** | Loading Bay | Optional story beat. A voice on an abandoned walkie-talkie warns the player about surveillance and sets a flag that can influence ending dialogue. |

---

## Inventory Items

| Item | What It Is Used For |
|------|---------------------|
| **Keycard** | Unlocks the loading bay exit door — required for Ending 1 |
| **Emergency Badge** | Grants Level 2 emergency clearance — flavor item that confirms identity at security scanners |
| **Access Code: 7-7-DELTA** | Opens the maintenance tunnel door — required for Ending 3 |
| **Vending Snacks** | Distracts the guard dog at Lab C — required to clear the guard dog challenge |
| **First Aid Kit** | Restores up to 30 HP to the player. Consumable. |

All items are viewable at any time through the in-game action menu (press `M` → option 1).

---

## Challenges

### Challenge 1 — Terminal Login
- **Where it occurs:** Server Room (Path 2)
- **What the player must do:** Enter the correct password into the facility terminal. The password is the year the facility opened (`2019`) plus the director's initials (`MV`), giving `2019MV`. The player gets 3 attempts before the terminal locks them out. Clues are available from ARIA (password format) and from a sticky note found by looking around the server room (year + director name).
- **On success:** Alarms are disabled, the security checkpoint unlocks, and the player proceeds toward Ending 2.
- **On failure:** After three wrong attempts the terminal locks out for the session. The player can return later and try again.

### Challenge 2 — Guard Dog
- **Where it occurs:** Lab C / Maintenance Tunnel (Path 3)
- **What the player must do:** Get past a guard dog blocking the maintenance tunnel. The intended solution is to bring Vending Snacks from the break room and throw them as a distraction. Without snacks, the player can attempt to sneak, run, or back away — but only backing away is safe (running costs 20 HP).
- **On success (with snacks):** The dog chases the snacks, the player escapes through the tunnel, and reaches Ending 3.
- **On failure (no snacks):** The player must back away and head to the vending machine to find a distraction before retrying.

---

## Cyber Pack — Required Cybersecurity Features

The game implements all three required Cyber Pack features:

### 1. Input Validation + Safe Error Handling
Every input prompt is wrapped in `try`/`except` logic that catches non-integer input, out-of-range numbers, and empty input. When invalid input is detected, the game prints a clear error message and re-prompts the player instead of crashing. This applies to the main menu, scene choices, NPC interactions, action menu, terminal login attempts, and the guard dog challenge.

Implemented in `security/security.py` via the `get_valid_number()` and `get_yes_or_no()` helper functions, and used directly by `main.py` and `engine/game_engine.py`.

### 2. Audit Logging to `audit_log.txt`
Every security-relevant event is written to `audit_log.txt` with an ISO-formatted timestamp. Logged events include:
- Program start and end
- Game start and end (including which ending was reached)
- All scene transitions and choices made
- NPC interactions
- Challenge attempts (with success/failure result and number of attempts)
- Save and load attempts (with success/failure result)
- Every invalid input the player enters
- Item use events

Example log line:
```
2026-05-13 14:37:42 - CHALLENGE_ATTEMPT - SUCCESS - Puzzle=terminal_login
```

Implemented in `security/security.py` via the `log_event()` function.

### 3. Save/Load With SHA-256 Tamper Detection
When the player saves the game, the entire game state is serialized to `savegame.json` along with a SHA-256 hash computed from a stable JSON representation of the state. When the game is loaded:
1. The save file is read and parsed
2. The hash is recomputed from the loaded state
3. The new hash is compared to the stored hash
4. If they don't match, the save is rejected with the message "Save file was tampered with. Load rejected." and the player must start a new game

This prevents players from editing their `savegame.json` to give themselves more HP or items. Implemented in `security/save_load.py`.

---

## In-Game Action Menu
At any scene during gameplay, type `M` to open the action menu:
1. View Inventory — Shows all collected items with descriptions
2. Use an Item — Apply an item's effect (e.g., First Aid Kit restores HP)
3. Save Game — Save current progress to `savegame.json` with hash
4. Player Status — Show health, current scene, items, and active flags
5. Back to Game — Return to the current scene
6. Quit Game — Exit to main menu (with confirmation prompt)

---

## File Structure
```
main.py                      # Entry point + main menu
README.md                    # This file
docs/
    flowchart.png            # Story branching flowchart
content/
    story.py                 # Scene definitions, branching logic
    npcs.py                  # NPC dialogue and interactions
engine/
    game_engine.py           # Scene runner, menus, input loop
    state.py                 # Game state creation + summary
systems/
    inventory.py             # Item definitions, add/remove/use
    challenges.py            # Terminal Login + Guard Dog puzzles
security/
    security.py              # Input validation + audit logging
    save_load.py             # SHA-256 save/load with tamper check
```

Generated at runtime: `audit_log.txt`, `savegame.json`
