# Python Game Project

This project is a 2D action/top-down game built using Pygame.

## 🎮 Overview
The game features a top-down perspective, allowing the player to move and explore a dynamic tile-based world. Key mechanics include:
*   **Movement:** Standard movement across various tile types (Grass, Dirt, Sand, Water).
*   **Combat:** Basic combat system involving the player's sword attacks and enemy AI.
*   **Progression:** A level/XP system where players gain experience to level up.
*   **World:** A tile-based map system managed by `TileMap`, featuring walls, water, and collectible/interactive elements.

## 🕹️ Getting Started

### Prerequisites
You will need Python installed on your system.

### Installation
1. Clone the repository:
   ```bash
   git clone [REPOSITORY_URL]
   cd python_game
   ```
2. Create and activate a virtual environment (Recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Linux/macOS
   # .\venv\Scripts\activate   # On Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Game
Run the main application file:
```bash
python main.py
```

## 🗺️ Code Structure

*   **`main.py`**: The application entry point, handling initialization and the main game loop.
*   **`game.py`**: Contains the primary game logic, state management (play, dead, etc.), and event handling.
*   **`tilemap.py`**: Implements the tile map system, handling world geometry, rendering, and collision detection.
*   **`settings.py`**: Stores global constants and configurations (e.g., screen dimensions, tile sizes, damage values).
*   **`player.py`**: Manages the player character's state, movement, and interaction logic.
*   **`enemies.py`**: Manages all enemy entities, including their AI and combat responses.

## ✨ Features
*   **Tile-Based Rendering:** Dynamic drawing of tiles, including animated water effects.
*   **Collision Detection:** Robust system to determine which tiles block movement.
*   **Visual Effects:** Particle effects and floating text for damage and experience.
*   **Level Progression:** XP and leveling mechanics are implemented.

## 🤝 Contributing
Feel free to open issues or submit pull requests with improvements or new features!
