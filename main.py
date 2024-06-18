import random
import time
import tkinter
import tkinter as tk
from tkinter import NW

from tank import *
from PIL import Image, ImageTk, ImageDraw
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
        self.num_tanks = 2
        self.root = root
        self.root = root
        self.root.geometry(f"{WIDTH}x{HEIGHT}")  # Set the size of the root window to match the canvas size

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
        self.canvas.pack()
        self.terrain_tk_image = None  # Keep a reference to the PhotoImage object
        self.current_player = 0

        self.scale_widget = None
        # Create Play button
        self.button_frame = tk.Frame(root)
        self.button_frame.place(relx=0.5, rely=0.5, anchor='center')  # Center the frame

        # Create Play button with custom size
        self.play_button = tk.Button(self.button_frame, text="Play", command=self.start_game, width=20, height=2)
        self.play_button.grid(row=0, column=0, padx=10, pady=10)

        # Create Hall of Fame button with custom size
        self.hall_of_fame_button = tk.Button(self.button_frame, text="Hall of Fame", command=self.show_hall_of_fame,
                                             width=20,
                                             height=2)
        self.hall_of_fame_button.grid(row=1, column=0, padx=10, pady=10)
        self.scale_widget = tk.Scale(self.button_frame, from_=2, to=4, orient=tk.HORIZONTAL, command=self.set_num_tanks)
        self.scale_widget.set(self.num_tanks)  # Set initial value
        self.scale_widget.grid(row=2, column=0, padx=10, pady=10)  # Center the slider

        self.trajectory_points = []
        self.projectile_active = False
        self.colors = ['red', 'black', 'yellow', 'purple']
        # Hide the canvas initially
        self.canvas.pack_forget()

    def show_hall_of_fame(self):
        pass

    def set_num_tanks(self, value):
        # Update the number of tanks based on the slider's value
        self.num_tanks = int(value)

    def start_game(self):
        self.scale_widget.destroy()
        self.scale_widget = None
        self.button_frame.destroy()
        # Show the canvas and call setup_game with the selected number of tanks
        self.canvas.pack()
        self.setup_game(num_tanks=self.num_tanks)

    def setup_game(self, num_tanks):
        print("num_tanks", num_tanks)
        self.terrain_image = self.generate_terrain()
        self.draw_terrain()

        # Calculate evenly spaced x positions for tanks
        spacing = WIDTH // (num_tanks)
        # spawn_positions = [50]
        # spawn_positions += [(i * spacing) for i in range(1,num_tanks+1)]
        spawn_positions = [(i * spacing + spacing//2) for i in range(0,num_tanks)]
        spawn_positions[-1] += spacing // 4
        spawn_positions[0] -= spacing // 4
        self.tanks = []
        for i in range(num_tanks):
            tank = self.spawn_tank(spawn_positions[i], f"{self.colors[i]}")
            self.tanks.append(tank)

        for tank in self.tanks:
            tank.draw()

        self.root.bind('<Up>', lambda event: self.control_power(dir=1))
        self.root.bind('<Down>', lambda event: self.control_power(dir=-1))
        self.root.bind('<Left>', lambda event: self.move_turret(dir=1))
        self.root.bind('<Right>', lambda event: self.move_turret(dir=-1))
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
            altitude = map_value(altitude, -1, 1, MIN_ALTITUDE, MAX_ALTITUDE)
            for y in range(WORLD_HEIGHT):
                if y > altitude:
                    terrain.putpixel((x, y), TERRAIN_COLOR)
                else:
                    terrain.putpixel((x, y), (136, 206, 235))
        return terrain

    def draw_terrain(self):
        self.canvas.delete('terrain')
        self.terrain_image = self.terrain_image.resize(
            (WORLD_WIDTH * SCALE_FACTOR, WORLD_HEIGHT * SCALE_FACTOR), Image.NEAREST)
        self.terrain_tk_image = ImageTk.PhotoImage(self.terrain_image)

        # Display the image on the canvas
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.terrain_tk_image, tags="terrain")

    def spawn_tank(self, spawn_x, color):
        # Find the exact altitude for the tank's base at the given spawn_x
        noise_value = pnoise1(spawn_x * NOISE_SCALE, octaves=OCTAVES)
        base_altitude = int(map_value(noise_value, -1, 1, MIN_ALTITUDE, MAX_ALTITUDE))

        # Adjust base altitude to ensure the tank is placed on the terrain
        while self.terrain_image.getpixel((spawn_x, base_altitude)) != TERRAIN_COLOR:
            base_altitude += 1  # The y-coordinate just above the terrain

        tank_y_position = int(base_altitude) - (TANK_SIZE // 2)

        # Clear space for the tank
        for x in range(spawn_x - TANK_SIZE // 2, spawn_x + TANK_SIZE // 2):
            for y in range(tank_y_position, int(base_altitude)):
                if 0 <= x < self.terrain_image.width and 0 <= y < self.terrain_image.height:
                    self.terrain_image.putpixel((x, y), TERRAIN_COLOR)

        return Tank(Pos(spawn_x, tank_y_position), color, self.canvas)

        # self.draw_terrain()
        # return Tank(Pos(spawn_x, tank_y_position), color, self.canvas)

    def move_turret(self, dir):
        self.tanks[self.current_player].rotate_turret(dir * 5)
        self.tanks[self.current_player].update_ui()  # Update the UI elements

    # self.end_turn()

    # self.end_turn()
    def end_turn(self):
        if len(self.tanks) > 0:
            self.current_player = (self.current_player + 1) % len(self.tanks)
            self.tanks[self.current_player].update_ui()  # Update the UI elements for the new current player

    def fire_projectile(self):
        if not self.projectile_active:
            velx = self.tanks[self.current_player].power * math.cos(math.radians(self.tanks[self.current_player].angle))
            vely = -self.tanks[self.current_player].power * math.sin(
                math.radians(self.tanks[self.current_player].angle))
            p = projectile.Projectile(
                Pos(self.tanks[self.current_player].turret_end.x,
                    self.tanks[self.current_player].turret_end.y - TANK_SIZE),
                Pos(velx, vely), self.tanks[self.current_player].color, 30, self.canvas)
            self.prev_seconds = time.time()
            self.trajectory_points = [(p.pos.x, p.pos.y)]  # Initialize the trajectory points list
            self.projectile_active = True
            self.tanks[self.current_player].shots += 1
            self.animate_projectile(p)
            print([(i, tank.score) for i, tank in enumerate(self.tanks)])

    def animate_projectile(self, projectile):
        gravity = 9.8  # Acceleration due to gravity
        time_interval = .05 # Time step for the simulation

        # Update horizontal position
        projectile.pos.x += projectile.vel.x * time_interval

        # Update vertical position
        projectile.pos.y += projectile.vel.y * time_interval + 0.5 * gravity * (time_interval ** 2)

        # Update vertical velocity
        projectile.vel.y += gravity * time_interval

        # Update projectile position on canvas
        self.canvas.coords(projectile.projectile, projectile.pos.x - projectile.ball_size,
                           projectile.pos.y - projectile.ball_size,
                           projectile.pos.x + projectile.ball_size, projectile.pos.y + projectile.ball_size)

        # Append the new position to the trajectory points list
        self.trajectory_points.append((projectile.pos.x, projectile.pos.y))
        # Draw the trajectory line
        if len(self.trajectory_points) > 1:
            self.canvas.create_line(self.trajectory_points[-2], self.trajectory_points[-1], fill=projectile.color,
                                    width=2)

        if not (0 <= projectile.pos.x <= (WORLD_WIDTH * SCALE_FACTOR)):
            print(projectile.pos.x, projectile.pos.y)
            projectile.vel.x *= -1
        elif not (0 <= projectile.pos.y <= (WORLD_HEIGHT * SCALE_FACTOR)):
            print(projectile.pos.x, projectile.pos.y)
            projectile.vel.y *= -1
        elif self.check_collision(projectile):
            self.create_crater(projectile.pos.x, projectile.pos.y, projectile.explosion_radius)
            self.canvas.delete(projectile.projectile)
            self.projectile_active = False
            self.end_turn()
            return
        self.canvas.after(int(time_interval * 100), self.animate_projectile, projectile)

    def check_collision(self, projectile):
        if self.terrain_image.getpixel((projectile.pos.x, projectile.pos.y)) == TERRAIN_COLOR:
            return True
        return False

    def create_crater(self, x, y, radius):
        for tank in self.tanks:
            self.canvas.delete(tank.id)
            self.canvas.delete(tank.turret)
        draw = ImageDraw.Draw(self.terrain_image)
        # Draw a filled circle to simulate the crater, filling it with sky color (assuming sky color is blue)
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=(135, 206, 235))  # Assuming sky blue color

        for i, tank in enumerate(self.tanks):
            if x - radius <= tank.pos.x <= x + radius:
                tank.lives -= 1
                if i != self.current_player:
                    shots = self.tanks[self.current_player].shots
                    # if tank managed to hit an opponent on nth attempt, aims to award accuracy
                    if shots == 1:
                        self.tanks[self.current_player].score += 20
                    elif shots == 2:
                        self.tanks[self.current_player].score += 15
                    else:
                        self.tanks[self.current_player].score += 10
            if tank.lives == 0:
                self.tanks.remove(tank)

        self.update_canvas()

        for tank in self.tanks:
            self.drop_tanks(tank)

        if len(self.tanks) == 1:
            ui_text = f"{self.tanks[-1].color} won"
            self.canvas.create_text(WORLD_WIDTH//2, WORLD_HEIGHT//2, text=ui_text, fill=self.tanks[-1].color,
                                                      font=('Helvetica', '50', 'bold'), anchor='center')

    def drop_tanks(self, tank):
        x = tank.pos.x
        y = tank.pos.y + 1
        if y == HEIGHT:
            tank.lives = 0
            self.tanks.remove(tank)
        elif self.terrain_image.getpixel((x, y)) != TERRAIN_COLOR:
            tank.update_tank(Pos(x, y))
            self.canvas.after(int(.05 * 100), self.drop_tanks, tank)

    def update_canvas(self):
        self.tk_image = ImageTk.PhotoImage(self.terrain_image)
        self.canvas.create_image(0, 0, anchor=NW, image=self.tk_image)

        # Redraw the tanks and other objects to maintain their visibility
        for tank in self.tanks:
            tank.draw()

    def control_power(self, dir):
        self.tanks[self.current_player].update_power(dir * 10)
        self.tanks[self.current_player].update_ui()  # Update the UI elements
        print("power", self.current_player, self.tanks[self.current_player].power)


if __name__ == "__main__":
    root = tk.Tk()
    app = ScorchedEarth(root)
    root.mainloop()
