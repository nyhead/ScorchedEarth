# Constants
import math

WIDTH = 1024
HEIGHT = 720
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
class Pos:
    def __init__(self,x,y):
        self.x = x
        self.y = y


def rotate(x, y, angle_degrees, turret_length):
    angle_radians = angle_degrees * math.pi / 180
    endx = x + turret_length * math.cos(angle_radians)
    endy = y - turret_length * math.sin(angle_radians)
    return endx, endy
# Enums for game state and projectile type
class State:
    AIM = 1
    POWER = 2
    RESOLVE = 3
    GAME_OVER = 4

class ProjectileType:
    REGULAR = "Regular"
    CLUSTER_BOMB = "Cluster"