# Galactic Gladiators

A turn-based strategy game built with Python and Pygame, where players command units in an epic space battle across a grid-based battlefield.

## Overview

Galactic Gladiators is a strategic turn-based game where you command various military units to defeat your AI opponent. The game features special terrain, unique unit abilities, and a persistent database system to save your progress.

## Features

- **Turn-Based Strategy Gameplay**: Command your units across a 10x10 grid battlefield
- **Multiple Unit Types**: Deploy 7 different unit types, each with unique abilities
- **Special Terrain**: Navigate elevated ground, coverage areas, sensor fields, and goldmines
- **AI Opponent**: Battle against an intelligent AI opponent
- **Save/Load System**: Save your progress and continue games later
- **Special Powers**: Units have unique special abilities that can turn the tide of battle
- **Cutscenes**: Enjoy cinematic cutscenes at the start and end of games
- **Background Music**: Immersive audio experience with different themes for menus and gameplay
- **Score System**: Track your victories and defeated units

## Installation

### Prerequisites

- Python 3.7 or higher
- MySQL Server
- pip (Python package manager)

### Required Python Packages

Install the required packages using pip:

```bash
pip install -r requirements.txt
```

### Database Setup

1. Import the SQL dump to create the database, tables, and initial data

2. Update the database configuration in `config.py`:

```python
config = {
    "host": "localhost",
    "user": "root",
    "password": "your_password",
    "database": "galactic_gladiators"
}
```

3. The game will automatically create the necessary tables on first run (assuming your DAO classes handle table creation, or you may need to run a database schema script if provided).

## Usage

### Starting the Game

Run the main game file:

```bash
python main.py
```

### Game Controls

- **Mouse Click**: Select and move units, attack enemies
- **C Key**: Toggle cheat mode (if enabled)
- **M Key**: Toggle music volume
- **Escape/Close Window**: Exit the game

### Gameplay

1. **Main Menu**: Choose to start a new game or load a saved game
2. **Nickname Input**: Enter your player nickname
3. **Game Board**: Command your units to move and attack
4. **Victory/Defeat**: Complete objectives to win the game

## Game Mechanics

### Unit Types

1. **Verkenner (Scout)**: Can become invisible for 3 turns
2. **Infanterist (Infantry)**: Basic combat unit
3. **Scherpschutter (Sniper)**: Can attack units up to 4 squares away with a chance to eliminate them
4. **Schilddrager (Shield Bearer)**: Can protect other units from enemy abilities
5. **Strijdmeester (Battle Master)**: Can increase the rank of adjacent friendly units
6. **Commando**: Can convert adjacent enemy units to friendly units
7. **Vlag (Flag)**: The objective unit - protect your flag and capture the enemy's flag

### Special Fields

- **Elevated (Blue)**: Provides +1 attack bonus
- **Coverage (Purple)**: Protects units from sniper attacks
- **Sensor (Red)**: Reveals invisible units
- **Goldmine (Yellow)**: Provides strategic advantage

### Combat System

- Combat is resolved by comparing unit ranks
- Units on elevated terrain receive a +1 bonus
- Special powers can influence combat outcomes
- Draws result in both units being eliminated

## Technologies Used

- **Python 3**: Core programming language
- **Pygame**: Game development framework
- **MySQL**: Database for game persistence
- **mysql-connector-python**: MySQL database connector

## Game States

The game uses a state machine with the following states:

- `MENU`: Main menu screen
- `NICKNAME_INPUT`: Player nickname input screen
- `LOAD_GAME`: Load saved game screen
- `CUTSCENE`: Cutscene playback
- `PLAYING`: Active gameplay

## Special Features

### Cheat Mode

Press `C` to toggle cheat mode, which will reveal unit ranks.

### Music Control

Press `M` to toggle music volume on/off.

### Save System

The game automatically saves your progress. You can load saved games from the main menu.

## Authors

- Hessel Visser
- Ben van der Weg
