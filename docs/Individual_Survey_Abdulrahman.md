# Individual Survey — Abdulrahman
CYSE-130 Final Project | Group 8 | Sector 8 Adventure Game

---

## 1. What did you personally do?

I served as **group leader, project architect, primary coder, and integrator** for Group 8 from start to finish.

### Project planning and architecture

When the project started, only the three Role 2 files (`story.py`, `npcs.py`, `inventory.py`) had been written. I designed the entire rest of the project from scratch, including:

- The full folder structure (`engine/`, `content/`, `systems/`, `security/`, `docs/`) and which files would live in each folder
- The function contracts each file would expose to the rest of the codebase (e.g. `run_challenge(key, game_state) → bool`, the exact `game_state` dictionary shape used everywhere)
- The dependency order — Raki's `state.py` had to finish first because everyone needed `game_state` to exist; Role 3 came last because it plugged into the engine via stubs
- The stub-import pattern that let the game run end-to-end even before Role 3 had written their files, so we wouldn't be blocked on each other

### Splitting tasks across all three roles and coordinating the team

I didn't just split work inside Role 1 — I split the work across **all three roles** so each of the 7 team members had a clearly defined file and scope. When the project started there was no internal division beyond the broad "Role 1 / Role 2 / Role 3" labels from the assignment sheet. I broke that down into 9 specific files and matched each one to the right person:

- **Role 1 — me, Rehan, Raki:** I assigned myself `engine/game_engine.py` (hardest — scene routing, NPC menu, action menu, challenge handoff, input validation), Rehan got `engine/state.py` (medium — game state, flags, summary), and Raki got `main.py` (entry point — main menu, How to Play, outer game loop). I took the hardest file deliberately as leader.
- **Role 2 — Nithin, Nawaf:** I split Role 2 between Nithin (`story.py` — the full branching story, 18 scenes, condition-based choices, effect handling) and Nawaf (`npcs.py` + `inventory.py` — all 5 NPCs and all 5 items with use-effect functions).
- **Role 3 — Sami, Bader:** I split Role 3 between Sami (`security.py` + `save_load.py` — audit logging plus SHA-256 tamper detection on saves) and Bader (`challenges.py` — the terminal login and guard dog challenges).

Beyond just assigning files, I coordinated the team throughout. I wrote a full Day 1 through Day 5 schedule with specific mini-goals for every teammate — when each file needed to be done, what each person should be working on each day, and which integration step depended on which. When teammates ran into questions or were unsure how their file should plug into the rest of the project, I was the point of contact who explained the function contracts, clarified what the `game_state` dictionary needed to look like, and made sure everyone understood that Raki's `state.py` had to finish first because every other file depended on `game_state` existing. I sent the team integration notes in Discord laying out exactly what each role needed to expose to the others so nothing would break when we merged.

### Code I wrote

**`engine/game_engine.py`** — the entire core game engine, including:
- `run_scene()` — main scene executor that renders text, shows NPC menu, routes player choice, dispatches challenges via `_handle_challenge()`, applies effects, returns the next scene key
- `_action_menu()` — the M-key side menu with 6 options (inventory, use item, save, status, back, quit) with quit confirmation
- `_get_player_choice()` — the validated input loop that re-prompts on bad input and routes M to the action menu
- `_npc_menu()` — NPC interaction prompt with the `T1/T2/T0` selection format
- `_use_item_menu()` — item-use sub-menu
- `_handle_challenge()` — the bridge to Role 3's challenge system with audit logging on START / SUCCESS / FAIL
- `_print_scene()`, `_print_choices()`, `_divider()` — UI rendering helpers

**`main.py`** — final merged version. Raki wrote an initial main.py with the menu structure (audit log viewer, credits screen) and Sami later wrote a second version with security wiring. I merged the best of both into one 6-option final.

**`engine/state.py`** — final integrated version after resolving naming conflicts between three teammates' drafts.

**`README.md`** — wrote the full project documentation hitting all 9 rubric sub-points (a–i).

**`docs/flowchart.png`** — wrote the matplotlib code to generate the branching story diagram.

### Integration and bug fixing

When teammates' files came in, I personally resolved the conflicts that kept the game from running:

- A three-way function naming conflict (`create_initial_state` vs `create_new_state` vs `new_game_state`) — standardized on one name with a backwards-compat alias
- Two competing `main.py` versions from Raki and Sami — merged into one
- A missing `audit_log_path` export that Raki's `main.py` needed from Sami's `security.py`
- Duplicate flag dictionaries between `state.py` and `story.py`
- `Vending Snacks` double-removal crash in Path 3 (challenge and effect both removed it)
- Three `Keycard` choices that set the flag but never gave the player the item
- First Aid Kit defined but unobtainable — added it to the vending_machine scene
- `SECTOR 7` → `SECTOR 8` text consistency to match the project name
- Duplicate item additions in `rescue_scientist` when the scene was revisited

### QA and submission

After every integration step I ran a full test suite covering all 9 file imports, game state creation, save/load with SHA-256 tamper detection, all 3 paths reaching their endings, item gating (e.g. guard dog needing snacks), bad input at every menu, and audit log generation. Caught and fixed roughly a dozen integration bugs that would have crashed the game on the professor's machine.

I also handled GitHub setup (created the repo, uploaded all files with correct folder structure, tagged the v1.0 release) and prepared the team info document and final Canvas submission.

---

## 2. What was one teamwork challenge your group faced, and how did you solve it?

The biggest challenge was **uncoordinated parallel work on shared files**. Two teammates (Raki and Sami) independently wrote their own version of `main.py`. Raki's version had a clean 5-option menu with audit log viewer and credits screen but used the function name `create_initial_state()`. Sami's version had stronger `try`/`except` wrapping and was wired to his security modules but used a different function name `create_new_state()`. A third teammate, Rehan, had written `state.py` with yet a third name, `new_game_state()`. None of the three files could import each other — the game crashed on startup.

I solved it in three steps. **First**, standardized on one function name (`create_new_state()`) across all files and added `create_initial_state` as a backwards-compatible alias so neither teammate's existing code needed changes. **Second**, merged the best parts of both `main.py` drafts into one final version — kept Sami's security wiring and Raki's audit log viewer + credits screen, and expanded to a 6-option menu. **Third**, communicated the decision openly in Discord with a clear explanation of what was kept from each version, so neither felt their work was discarded.

The lesson was that for a team this size, **clear file ownership and a single integrator are non-negotiable**. After this incident I made the rule that all integration changes would go through me, which prevented further parallel rewrites. If I had set that rule on Day 1 the conflict wouldn't have happened in the first place.

---

## 3. Teammate Contribution Scores (private — instructor only)

| Teammate | Score | Reason |
|---|---|---|
| Rehan Mohammed | 5 | Delivered `engine/state.py` with all required state-tracking flags. Responsive in Discord and submitted quickly when asked. |
| Raki Vijayakumar | 5 | Wrote the initial `main.py` with the menu structure (audit log viewer, credits screen) that became part of the final merged version. |
| Nithin Arvind | 5 | Built the entire branching story system in `story.py` — 18 scenes, condition-based choices, and effect handling. Story structure was solid and integrated cleanly into the engine. |
| Nawaf Alqahtani | 5 | Built `npcs.py` and `inventory.py` with use-effect functions for all 5 items and all 5 NPCs. Well-documented, easy to integrate. |
| Sami Alwattar | 5 | Excellent work on `security.py` and `save_load.py`. Implemented SHA-256 tamper detection cleanly. Files were well-structured and integrated easily with the engine. |
| Bader Alansari | 5 | Built `challenges.py` with `terminal_login`, `guard_dog`, and a bonus `drone_patrol` challenge. All challenges followed the agreed-upon function signature so the engine could route to them without modification. |
