# Constants
WIDTH = 1000
HEIGHT = 750
SCALE_FACTOR = 3
WORLD_WIDTH = int(WIDTH / SCALE_FACTOR)
WORLD_HEIGHT = int(HEIGHT / SCALE_FACTOR)
TANK_SIZE = 10
NOISE_SCALE = .01
GRAVITY = (0, 0.2)
TERRAIN_COLOR = (30, 180, 60)

# Enums for game state and projectile type
class State:
    AIM = 1
    POWER = 2
    RESOLVE = 3
    GAME_OVER = 4

class ProjectileType:
    REGULAR = "Regular"
    CLUSTER_BOMB = "Cluster"