class Constants:
    # Screen dimensions
    SCREEN_WIDTH, SCREEN_HEIGHT = 1400, 980

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    ENEMY_BLUE = (0, 0, 255)
    GREEN = (102, 255, 102)
    BLUE = (80, 190, 150)  # Elevated
    PURPLE = (128, 0, 128)  # Coverage
    RED = (255, 0, 0)  # Sensor
    YELLOW = (255, 255, 0)  # Goldmine
    ORANGE = (255, 165, 0)  # Friendly Unit
    DEFAULT_INNER_COLOR = (255, 255, 204)
    BORDER_COLOR = (0, 0, 0)
    ATTACK_COLOR = (252, 101, 101)

    # Fonts
    FONT = None
    SMALL_FONT = None
    FONT_SIZE_LARGE = 74
    FONT_SIZE_MEDIUM = 24
    FONT_SIZE_SMALL = 50
    FONT_SIZE_RANK = 36

    # Game settings
    GRID_SIZE = 10
    FPS = 60
    SCROLL_SPEED = 20

    # Field types and counts
    FIELD_TYPES = ['elevated', 'coverage', 'sensor', 'goldmine']
    FIELD_COUNTS = {'elevated': 3, 'coverage': 2, 'sensor': 4, 'goldmine': 3}
    SPECIAL_FIELD_POSITIONS = [(row, col) for row in range(4, 8) for col in range(1, 11)]
    ENEMY_UNIT_POSITIONS = [(row, col) for row in range(9, 11) for col in range(1, 11)]

    # Unit counts
    UNIT_COUNTS = {1: 3, 2: 7, 3: 3, 4: 2, 5: 2, 6: 2, 7: 1}

    # Unit names
    UNIT_NAMES = {
        1: "Verkenner",
        2: "Infanterist",
        3: "Scherpschutter",
        4: "Schilddrager",
        5: "Strijdmeester",
        6: "Commando",
        7: "Vlag"
    }

    FLAG_ID = 7
    ENEMY_ABILITY_ODDS = 0.05
