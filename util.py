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
SKY_COLOR = (136, 206, 235)
MIN_ALTITUDE = .4 * WORLD_HEIGHT
MAX_ALTITUDE = .8 * WORLD_HEIGHT
CRATER_SIZE = 40
class Pos:
    def __init__(self,x,y):
        self.x = x
        self.y = y

def map_value(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def rotate(x, y, angle_degrees, turret_length):
    angle_radians = angle_degrees * math.pi / 180
    endx = x + turret_length * math.cos(angle_radians)
    endy = y - turret_length * math.sin(angle_radians)
    return endx, endy
