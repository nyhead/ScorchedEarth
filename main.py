import tkinter as tk
from tank import *
from PIL import Image, ImageTk
from noise import pnoise1
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
		self.setup_game()

	def setup_game(self):
		terrain_image = self.generate_terrain()
		self.draw_terrain(terrain_image)
		tank1 = self.spawn_tank(300, "red")
		tank2 = self.spawn_tank(500, "purple")
		self.tanks.append(tank1)
		self.tanks.append(tank2)
		for tank in self.tanks:
			tank.draw()

	def generate_terrain(self):
		terrain = Image.new("RGB", (WORLD_WIDTH, WORLD_HEIGHT))

		for x in range(WORLD_WIDTH):
			altitude = map_value(pnoise1(x * NOISE_SCALE, octaves=6), 0, 1, 0.2 * WORLD_HEIGHT,
								 0.8 * WORLD_HEIGHT)
			for y in range(WORLD_HEIGHT):
				if y > altitude:
					terrain.putpixel((x, y), TERRAIN_COLOR)

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
		noise_value = pnoise1(spawn_x * NOISE_SCALE, octaves=6)
		altitude = int(map_value(noise_value, 0, 1, 0.2 * WORLD_HEIGHT, 0.8 * WORLD_HEIGHT)) + 100
		print(int(altitude + TANK_SIZE // 2))
		# Clear terrain area for the tank

		for x in range(spawn_x - TANK_SIZE, spawn_x + TANK_SIZE):
			depth = TANK_SIZE
			for y in range(WORLD_HEIGHT,altitude,-1):
				if self.terrain_image.getpixel((x, y)) != TERRAIN_COLOR:
					self.terrain_image.putpixel((x, y), TERRAIN_COLOR)  # Clear the space for the tank

		self.draw_terrain(self.terrain_image)
		return Tank(Pos(spawn_x, altitude), color, self.canvas)

if __name__ == "__main__":
	root = tk.Tk()
	app = ScorchedEarth(root)
	root.mainloop()
