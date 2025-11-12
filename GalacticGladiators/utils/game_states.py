from enum import Enum


class GameState(Enum):
    MENU = 1
    NICKNAME_INPUT = 2
    LOAD_GAME = 3
    PLAYING = 4
    CUTSCENE = 5
