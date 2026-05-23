# ⚔️ Elemental Brawl

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Status](https://img.shields.io/badge/Status-Stable-brightgreen?style=for-the-badge)

> *"Three heroes. Three elements. One terminal. No mercy."*

A turn-based RPG combat engine built in pure Python — demonstrating object-oriented design, state management, and terminal UI architecture through an elemental magic system. No frameworks. No dependencies. Just standard library, clean class hierarchies, and a combat loop that actually works.

---

## 📌 What This Is

A fully playable terminal RPG featuring:

- **Turn-based combat** — 3-player party vs 3-enemy encounter with sequential action resolution
- **Elemental magic system** — Black magic (Fire, Thunder, Blizzard, Meteor, Quake) and White magic (Cure, Cura) with MP costs and type-based targeting logic
- **Inventory management** — Consumable potions, elixirs, and attack items with quantity tracking
- **Enemy AI** — Probabilistic spell selection with MP-awareness and self-preservation heuristics
- **Terminal UI** — Color-coded output, dynamic HP/MP bars, and formatted stat displays using ANSI escape sequences
- **State persistence** — Live HP/MP tracking, death handling, and win/lose condition evaluation across the combat loop

Single `main.py` entry point. Run and fight. No installation ritual required.

---

## 🏗️ Architecture

```
main.py
  ├── classes/
  │   ├── game.py          # Person class — combatant state, actions, UI rendering
  │   ├── magic.py         # Spell class — damage generation, cost, type classification
  │   └── inventory.py     # Item class — consumable properties and effects
  └── Game loop            # Turn resolution, targeting, win/lose evaluation
```

---

## 🎯 Why This Design

### Why Pure Python / Zero Dependencies

Every dependency is a liability in a learning project. `random` for damage variance. `os` for Windows color support. That is the entire external surface. No `curses`, no `rich`, no `colorama` — because the goal was to understand how terminal control sequences actually work, not how a library abstracts them away.

The tradeoff: manual ANSI escape code management and cross-platform encoding handling. The win: knowing exactly why `\033[91m` turns text red and why Windows CMD needs `os.system("color")` before it will interpret it.

### Why Composition Over Inheritance for Combatants

`Person` encapsulates both player and enemy behavior. Early drafts had separate `Player` and `Enemy` subclasses, but the divergence was minimal — both have HP, MP, attack ranges, spell lists, and damage methods. The real difference is decision-making:

- **Player**: `input()`-driven action selection with target choice
- **Enemy**: `random`-driven action selection with heuristic spell filtering

This was solved by keeping `Person` unified and letting the game loop handle whose turn it is — not by forcing an inheritance hierarchy that would have introduced `super()` complexity for two methods that differ by 4 lines. Composition via the `actions` list and external turn logic proved cleaner than subclassing for behavior that is 95% identical.

### Why a Three-Layer Combat Loop

```
Player Phase (sequential, each player acts)
  → Action selection (Attack / Magic / Inventory)
  → Target resolution (enemy selection for offensive, self for healing)
  → State mutation (HP/MP changes, death checks, inventory decrement)
  → Win condition evaluation (all enemies dead?)

Enemy Phase (sequential, each enemy acts)
  → AI decision (physical attack or spell)
  → Target resolution (random player selection)
  → State mutation (HP changes, death checks)
  → Lose condition evaluation (all players dead?)
```

Separating player and enemy phases prevents interleaving chaos and makes the combat log readable. Sequential resolution within each phase means players can coordinate — one heals while another attacks — without race conditions or priority systems.

### Why ANSI Colors Over a TUI Library

`bcolors` is 12 lines of class variables. It works in every terminal that supports ANSI — which is every modern terminal, including Windows Terminal, VS Code integrated terminal, and CMD after `color` initialization. The alternative (`curses`, `blessed`, `rich`) would add 500+ lines of abstraction for a problem that 12 lines solves directly.

The block character `█` was replaced with `#` after discovering Windows CMD defaults to `cp1252` encoding, which cannot map Unicode U+2588. This is documented not as a workaround but as a platform constraint that every cross-platform CLI project eventually encounters.

---

## ⚔️ Combat System

### Action Economy

| Action | Cost | Target | Notes |
|--------|------|--------|-------|
| **Attack** | None | Single enemy | Damage = random(atk-10, atk+10) |
| **Magic** | MP | Single enemy (Black) / Self (White) | Spell cost deducted before cast |
| **Inventory** | Item quantity | Varies by item | Potions heal, elixirs restore, grenades damage |

### Magic System

**Black Magic** — Offensive, targets enemies, damage variance ±15

| Spell | MP Cost | Base Damage | Element |
|-------|---------|-------------|---------|
| Fire | 10 | 1000 | Fire |
| Thunder | 12 | 1200 | Lightning |
| Blizzard | 14 | 1400 | Ice |
| Meteor | 16 | 1600 | Cosmic |
| Quake | 20 | 2000 | Earth |

**White Magic** — Restorative, targets self, healing variance ±15

| Spell | MP Cost | Base Heal |
|-------|---------|-----------|
| Cure | 12 | 1200 |
| Cura | 40 | 4000 |

> MP is a hard gate. A player at 10 MP cannot cast Thunder (12 cost) — the action fails before damage is rolled. This creates resource tension: save MP for clutch heals, or burn it early for damage spikes?

### Inventory

| Item | Effect | Quantity |
|------|--------|----------|
| Potion | Heal 50 HP | 5 |
| Hi-Potion | Heal 100 HP | 5 |
| Super-Potion | Heal 150 HP | 5 |
| Elixir | Full HP/MP restore (self) | 5 |
| MegaElixir | Full HP/MP restore (all allies) | 5 |
| Grenade | Deal 500 damage to one enemy | 5 |

> Quantity is checked **before** decrement. A player at 0 potions sees `"Not Enough potions"` and loses their turn — a tactical penalty for poor resource tracking.

### Enemy AI

Enemies select between physical attack (50%) and magic (50%). Spell selection uses recursive filtering:

1. **MP gate**: Cannot cast if `current_mp < spell.cost`
2. **Self-preservation**: Will not cast White magic if `hp/max_hp > 50%`
3. **Fallback**: If no spells satisfy constraints, defaults to physical attack

This prevents enemies from healing at full health or attempting unaffordable spells — common AI failures in early RPG implementations.

---

## 🎮 Gameplay

```bash
python main.py
```

```
AN ENEMY ATTACKS!
=======================
  NAME                       HP                                   MP
                             _________________________            ____________________
 Valos  :         3000/3000 |#########################|   125/125|####################|
                             _________________________            ____________________
 Abhi   :         4000/4000 |#########################|   150/150|####################|
                             _________________________            ____________________
 Raj    :         3500/3500 |#########################|   140/140|####################|
                             ____________________________________________________
 Dragon         15000/15000 |##################################################|
                             ____________________________________________________
 Reek             1250/1250 |##################################################|
                             ____________________________________________________
 Reek-II          1250/1250 |##################################################|

    Valos  :
     ACTIONS:
     1:Attack
     2:Magic
     3:Inventory
    Choose an action:
```

**Win condition**: All enemies defeated.  
**Lose condition**: All players defeated.

---

## 🛠️ Technical Decisions

### Why `random.randrange` for Damage

`randrange(low, high)` produces uniform integer distribution across the attack band. This creates predictable variance — a player with `atk=300` deals 290–310 damage, never 1 or 1000. The ±10 band is narrow enough to feel fair, wide enough to prevent deterministic outcomes.

### Why Circular HP/MP Clamping

```python
def take_damage(self, dmg):
    self.hp -= dmg
    if self.hp <= 0:
        self.hp = 0

def heal(self, dmg):
    self.hp += dmg
    if self.hp > self.maxhp:
        self.hp = self.maxhp
```

No negative HP. No overhealing. State invariants are enforced at the mutation site, not trusted to callers. This prevents edge cases like a 500-damage grenade on a 50-HP enemy producing -450 HP and breaking death checks.

### Why `del` for Death Handling

Dead combatants are removed from the list (`del enemies[index]`). This simplifies targeting — the `choose_target` method only presents living enemies — but introduces list mutation during iteration. The enemy phase iterates over a snapshot (`for enemy in enemies:`) and the list is only modified during the player phase, preventing `RuntimeError: dictionary changed size during iteration`.

> A production implementation would use object pools or tombstoning (`is_alive` flags) instead of list deletion. For a terminal RPG with 6 total combatants, `del` is readable and sufficient.

---

## 📁 Project Structure

```
elemental-brawl/
├── classes/
│   ├── __init__.py      # Package exports
│   ├── game.py          # Person class, bcolors, combatant state
│   ├── magic.py         # Spell class, damage generation
│   └── inventory.py     # Item class, consumable definitions
├── main.py              # Game initialization, combat loop, win/lose logic
└── README.md
```

---

## 🚀 Quick Start

### Requirements

- Python 3.10+
- Windows: CMD or PowerShell (ANSI colors auto-enabled)
- macOS/Linux: Any terminal emulator

### Run

```bash
# Clone or download
cd elemental-brawl

# Play
python main.py
```

No virtual environment. No `requirements.txt`. No `pip install`. The entire dependency graph is the Python standard library.

---

## 🧪 What This Demonstrates

`OOP` `Encapsulation` `Composition` `State Management` `Game Loop Architecture`
`ANSI Terminal Control` `Cross-Platform CLI` `Python Standard Library`

---

## 📋 License

MIT — fork it, break it, rebuild it.

---

## 🙏 Acknowledgements

- **Python `random` module** — for damage variance that feels fair
- **ANSI escape codes** — for making terminals colorful since 1979
- **Windows `color` command** — for reluctantly supporting color in CMD
- Every RPG that ever made you ration MP before a boss fight
