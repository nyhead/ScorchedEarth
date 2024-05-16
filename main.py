import random
import tkinter as tk
from tank import *
from PIL import Image, ImageTk
from noise import pnoise1, pnoise2
from game_state import *

def map_value(value, leftMin, leftMax, rightMin, rightMax):
	# Figure out how 'wide' each range is
	leftSpan = leftMax - leftMin
	rightSpan = rightMax - rightMin

	# Convert the left range into a 0-1 range (float)
	valueScaled = float(value - leftMin) / float(leftSpan)

	# Convert the 0-1 range into a value in the right range.
	return rightMin + (valueScaled * rightSpan)


class ScorchedEarth:
	def __init__(self, root):
		self.tanks = []
		self.root = root
		self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg='sky blue')
		self.canvas.pack()
		self.terrain_tk_image = None  # Keep a reference to the PhotoImage object
		self.current_player = 0
		self.setup_game()

	def setup_game(self):
		terrain_image = self.generate_terrain()
		self.draw_terrain(terrain_image)
		tank1 = self.spawn_tank(100, "red")
		tank2 = self.spawn_tank(2*WORLD_WIDTH - 100, "purple")
		self.tanks.append(tank1)
		self.tanks.append(tank2)
		for tank in self.tanks:
			tank.draw()

		self.root.bind('<Left>', lambda event: self.move_turret_left())
		self.root.bind('<Right>', lambda event: self.move_turret_right())
		self.root.bind('<space>', lambda event: self.fire_projectile())

	def generate_terrain(self):
		terrain = Image.new("RGB", (WORLD_WIDTH, WORLD_HEIGHT))
		seed = random.randint(0, 10000)  # Add randomness with a seed

		for x in range(WORLD_WIDTH):
			altitude = 0
			amplitude = 1
			frequency = NOISE_SCALE
			# Layer multiple frequencies of noise
			for _ in range(5):  # 5 layers of noise
				altitude += amplitude * pnoise1(x * frequency + seed)
				amplitude *= 0.5
				frequency *= 2
			altitude = map_value(altitude, -1, 1, MIN_ALTITUDE,MAX_ALTITUDE)
			for y in range(WORLD_HEIGHT):
				if y > altitude:
					terrain.putpixel((x, y), TERRAIN_COLOR)
		# for x in range(WORLD_WIDTH):
		# 	altitude = map_value(pnoise1(x * NOISE_SCALE, octaves=OCTAVES), 0, 1, MIN_ALTITUDE,MAX_ALTITUDE)
		# 	for y in range(WORLD_HEIGHT):
		# 		if y > altitude:
		# 			terrain.putpixel((x, y), TERRAIN_COLOR)
		terrain.save("terrain.png")
		return terrain

	def draw_terrain(self, terrain_image):
		self.canvas.delete('terrain')
		self.terrain_image = terrain_image.resize(
			(WORLD_WIDTH * SCALE_FACTOR, WORLD_HEIGHT * SCALE_FACTOR), Image.NEAREST)
		self.terrain_tk_image = ImageTk.PhotoImage(self.terrain_image)

		# Display the image on the canvas
		self.canvas.create_image(0, 0, anchor=tk.NW, image=self.terrain_tk_image, tags="terrain")

	def spawn_tank(self, spawn_x, color):
		# Find the exact altitude for the tank's base at the given spawn_x
		noise_value = pnoise1(spawn_x * NOISE_SCALE, octaves=OCTAVES)

		base_altitude  = int(map_value(noise_value, 0, 1, MIN_ALTITUDE, MAX_ALTITUDE))

		# altitude = 0
		while self.terrain_image.getpixel((spawn_x, base_altitude)) != TERRAIN_COLOR:
			base_altitude += 1  # The y-coordinate just above the terrain
		tank_y_position = int(base_altitude) - (TANK_SIZE // 2)
		for x in range(spawn_x - TANK_SIZE // 2, spawn_x + TANK_SIZE // 2):
			for y in range(tank_y_position, int(base_altitude)):
				if 0 <= x < self.terrain_image.width and 0 <= y < self.terrain_image.height:
					self.terrain_image.putpixel((x, y), TERRAIN_COLOR)  # Clear the space for the tank

		self.draw_terrain(self.terrain_image)
		return Tank(Pos(spawn_x, tank_y_position), color, self.canvas)

	def move_turret_left(self):
		self.tanks[self.current_player].rotate_turret(-5)
		# self.end_turn()

	def move_turret_right(self):
		self.tanks[self.current_player].rotate_turret(5)
		# self.end_turn()
	def fire_projectile(self):
		self.tanks[self.current_player].fire_projectile()
		self.end_turn()
	def end_turn(self):
		self.current_player = (self.current_player + 1) % len(self.tanks)


if __name__ == "__main__":
	root = tk.Tk()
	app = ScorchedEarth(root)
	root.mainloop()
