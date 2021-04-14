import pygame as py
py.font.init()


# =================== General constants ==================================
FPS = 90
WIN_WIDTH = 1800
WIN_HEIGHT = 1000
STARTING_POS = (WIN_WIDTH/2, WIN_HEIGHT-100)
SCORE_VEL_MULTIPLIER = 0.001  # Default: 0.00  # bonus for faster cars
BAD_GENOME_THRESHOLD = 200  # Default: 200  # if a car is too far behind it is removed (in px)
NO_GUI = False  # if True, no GUI will be shown
NO_NN = False  # if True, no best car NN will be shown

INPUT_NEURONS = 9  # Default: 9
OUTPUT_NEURONS = 4  # Default: 4

# =================== Car Specs ==================================

CAR_DBG = True  # Show car's sensors
FRICTION = -0.1  # Default: -0.1  # car speed decrease per frame
MAX_VEL = 10  # Default: 10  # max car speed per frame (in px)
MAX_VEL_REDUCTION = 1  # Default: 1, at the start reduce maximum speed
ACC_STRENGTH = 0.2  # Default: 0.2  # car speed increase on acceleration command
BRAKE_STRENGTH = 1  # Default: 1  # car speed decrease on brake command
TURN_VEL = 2  # Default: 2  # car angle change per frame (in radians)
SENSOR_DISTANCE = 200  # Default: 200
ACTIVATION_THRESHOLD = 0.5  # Default: 0.5  # value from output neurons threshold that activate control commands

# =================== Road Specs ==================================

ROAD_DBG = False  # show points instead lines
MAX_ANGLE = 1  # Default: 1
MAX_DEVIATION = 300  # Default: 300
SPACING = 200  # Default: 200
NUM_POINTS = 15  # Default: 15              # number of points for each segment
SAFE_SPACE = SPACING + 50  # Default: SPACING + 50       # buffer space above the screen
ROAD_WIDTH = 200  # Default: 200
ROAD_SEED = None  # Default: None  # if None road will be random each time, to fix one road change to any number or string

# =================== Display and Colors ==================================

NODE_RADIUS = 20  # Default: 20
NODE_SPACING = 5  # Default: 5
LAYER_SPACING = 100  # Default: 100
CONNECTION_WIDTH = 1  # Default: 1

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
DARK_RED = (100, 0, 0)
RED_PALE = (250, 200, 200)
DARK_RED_PALE = (150, 100, 100)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 100, 0)
GREEN_PALE = (200, 250, 200)
DARK_GREEN_PALE = (100, 150, 100)
BLUE = (0, 0, 255)
BLUE_PALE = (200, 200, 255)
DARK_BLUE = (100, 100, 150)

NODE_FONT = py.font.SysFont("comicsans", 15)
STAT_FONT = py.font.SysFont("comicsans", 50)


# =================== Constants for internal use ==================================
GEN = 0

# enumerations
ACC = 0
BRAKE = 1
TURN_LEFT = 2
TURN_RIGHT = 3

INPUT = 0
MIDDLE = 1
OUTPUT = 2
