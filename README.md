# 🚀 Space Shooter

A high-intensity arcade-style game built with Python and Pygame. Survive an endless barrage of meteors, rack up your score, and see how long you can last.

![Python](https://img.shields.io/badge/Python-3.x-blue) ![Pygame](https://img.shields.io/badge/Pygame-2.x-green) ![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

---

## 🎮 Gameplay

- Move your ship with the mouse for fluid, 1:1 control
- Shoot lasers to destroy incoming meteors
- Meteors spawn with randomised speed, rotation, and direction — and bounce off screen edges
- Survive as long as possible and aim for a high score

---

## 🛠️ Tech Stack

- **Language:** Python 3
- **Library:** Pygame

---

## 📁 Project Structure

```
space-shooter/
├── main.py          # Core game logic
└── assets/          # Sprites, fonts, sounds
```

---

## 🧱 Architecture

The project is built around OOP principles with all game entities inheriting from `pygame.sprite.Sprite`.

### Classes

**`Environment`**
Generates star objects that move vertically at varying speeds and loop when off-screen, creating a parallax scrolling effect that simulates high-speed space travel.

**`Objects`** *(Polymorphic)*
A single class handling three distinct entities via a `type` argument at initialisation:
- **Ship** — Player-controlled, position updated from mouse coordinates each frame
- **Meteor** — Spawns with randomised speed, rotation, and direction; bounces off screen edges
- **Laser** — Projectile fired by the player

**`Explosion`**
Iterates through a pre-loaded list of images frame-by-frame to animate meteor destruction, then calls `self.kill()` to remove itself from memory once the animation completes.

**`Scoreboard`**
Renders a live timer and hit counter using loaded font assets.

---

## ⚙️ Implementation Highlights

### State Machine
Game flow is managed via a `game_state` variable:
- `"main menu"` — Renders the start screen and waits for input
- `"gameplay"` — Initialises the game clock and runs the main physics/rendering loop

### Custom Event System
Meteor spawning uses `pygame.event.custom_type()` and `pygame.time.set_timer()` to fire a spawn event every 700–1000ms. This avoids polling every frame, keeping the game loop clean and performant.

### Collision Detection
Uses Pygame's sprite group collision methods:
- **Laser vs Meteor** — `pygame.sprite.spritecollide()` removes both sprites, triggers a sound effect, and spawns an `Explosion` object at the collision point
- **Ship vs Meteor** — Collision triggers the Game Over state

---

## 🚀 Getting Started

**Prerequisites**
```bash
pip install pygame
```

**Run the game**
```bash
python main.py
```

---

## 💡 Concepts Demonstrated

- Object-Oriented Programming (inheritance, polymorphism)
- Event-driven programming with custom Pygame events
- Real-time collision detection
- Sprite and animation management
- Basic game state machine
