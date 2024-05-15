# Constants
WIDTH = 600
HEIGHT = 400
SCALE_FACTOR = 2
WORLD_WIDTH = WIDTH // SCALE_FACTOR
WORLD_HEIGHT = HEIGHT // SCALE_FACTOR
TANK_SIZE = 6
NOISE_SCALE = .01
OCTAVES = 6
GRAVITY = (0, 0.2)
TERRAIN_COLOR = (30, 180, 60)
MIN_ALTITUDE = .4 * WORLD_HEIGHT
MAX_ALTITUDE = .8 * WORLD_HEIGHT
# Enums for game state and projectile type
class State:
    AIM = 1
    POWER = 2
    RESOLVE = 3
    GAME_OVER = 4

class ProjectileType:
    REGULAR = "Regular"
    CLUSTER_BOMB = "Cluster"