# Sector 8 — Text-Based Adventure Game
CYSE-130 Final Project | Spring 2026

## Team Members
- Abdulrahman (Role 1 — Core Engine)
- Rehan (Role 1 — Main / Game Loop)
- Raki (Role 1 — State Management)
- [Role 2 Nithin]
- [Role 2 Nawaf]
- [Role 3 Sami]
- [Role 3 Bader]

## How to Run
1. Make sure Python 3 is installed
2. Download or clone this repository
3. Open a terminal in the project folder
4. Run: python main.py

## Story Paths
1. **Find the Keycard** — Search the offices, interact with Guard Chen,
   collect a keycard and escape through the loading bay
2. **Hack the Terminal** — Access the server room, solve the terminal
   password puzzle, disable alarms and escape through the checkpoint
3. **Help the Scientist** — Follow cries for help, rescue Dr. Reyes,
   collect her items and escape through the maintenance tunnel

## Endings
1. **The Clean Escape** — Escape through the loading bay using the keycard
2. **The Ghost in the Wire** — Escape through the security checkpoint
   after hacking the terminal
3. **The Tunnel at Dawn** — Escape through the maintenance tunnel
   with Dr. Reyes after distracting the guard dog

## Locations / Events
1. **Sector 7 Lobby** — Starting point, three paths available
2. **Office Search** — Search for keycard, encounter Guard Chen
3. **Server Room** — Terminal puzzle, interact with ARIA
4. **East Corridor** — Find Dr. Reyes trapped under a shelf
5. **Lab C / Maintenance Tunnel** — Guard dog encounter, escape route

## NPCs
| NPC | Location | Role |
|-----|----------|------|
| Guard Chen | Office Search | Gives keycard clue, can be bribed or talked to |
| Dr. Reyes | East Corridor | Gives Emergency Badge and tunnel access code |
| Janitor Ko | Vending Machine | Gives Vending Snacks to distract the dog |
| ARIA | Server Room | Gives password format clue for terminal puzzle |
| Radio Voice | Loading Bay | Optional story beat, hints about safe exits |

## Inventory Items
| Item | Purpose |
|------|---------|
| Keycard | Unlocks the loading bay exit door |
| Emergency Badge | Grants Level 2 emergency clearance |
| Access Code 7-7-DELTA | Opens the maintenance tunnel door |
| Vending Snacks | Distracts the guard dog at Lab C |
| First Aid Kit | Restores 30 HP to the player |

## Challenges
1. **Terminal Login** (Server Room)
   - Player must guess the correct password
   - Format clue: year facility opened + director initials
   - Success: alarms disabled, checkpoint unlocked
   - Failure: player stays on scene and can retry

2. **Guard Dog** (Lab C)
   - Player must have Vending Snacks to pass
   - Success: dog distracted, tunnel accessible
   - Failure: player sent to find snacks first

## Cyber Pack
- **Input Validation** — All menus use try/except to catch invalid input.
  Players are always re-prompted instead of the game crashing.
- **Audit Logging** — All major events are written to audit_log.txt with
  timestamps including game start/end, choices made, challenge attempts,
  invalid inputs, and save/load attempts.
- **Save/Load with Tamper Detection** — Game progress is saved to
  savegame.json. A SHA-256 hash of the save data is stored alongside it.
  When loading, the hash is recomputed and compared. If the file was
  edited, the load is rejected and the player is forced to start over.
