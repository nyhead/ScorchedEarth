import random
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import pickle
from tank import Tank
from projectile import Projectile
from ui import GameUI
from util import *
from hall_of_fame import HallOfFame
import opensimplex
class ScorchedEarth:
    def __init__(self, root):
        self.root = root
        self.ui = GameUI(root, self.start_game, self.show_hall_of_fame, self.set_num_tanks)
        self.tanks = []
        self.num_tanks = 2
        self.current_player = 0
        self.projectile_active = False
        self.trajectory_points = []
        self.colors = ['red', 'blue', 'orange', 'purple']
        self.hol = self.load_hall_of_fame()
        self.terrain_tk_image = None

    def load_hall_of_fame(self):
        # Load hall of fame records from file, or create a new one if not found
        try:
            with open("hall_of_fame_record.pkl", "rb") as file:
                return pickle.load(file)
        except FileNotFoundError:
            return HallOfFame()

    def show_hall_of_fame(self):
        # Display the hall of fame window
        hall_of_fame_window = tk.Toplevel(self.root)
        hall_of_fame_window.title("Hall of Fame")
        hall_of_fame_window.geometry("300x400")
        tk.Label(hall_of_fame_window, text="Hall of Fame", font=('Helvetica', '20', 'bold')).pack(pady=10)
        for i, (name, score) in enumerate(self.hol.get_hall(), start=1):
            tk.Label(hall_of_fame_window, text=f"{i}. {name}: {score}").pack()

    def set_num_tanks(self, value):
        self.num_tanks = value

    def start_game(self):
        self.terrain_image = self.generate_terrain()
        self.draw_terrain()
        self.spawn_tanks()
        self.bind_controls()

    def generate_terrain(self):
        # Generate terrain using Perlin noise
        terrain = Image.new("RGB", (WORLD_WIDTH, WORLD_HEIGHT))
        tiny_noise = random.randint(0, 10000) # Add a bit more noise
        for x in range(WORLD_WIDTH):
            altitude = 0
            amplitude = 1
            frequency = NOISE_SCALE
            # Layer multiple frequencies of noise
            for _ in range(5):
                altitude += amplitude * opensimplex.noise2(x * frequency + tiny_noise, 0) # 5 layers of noise
                amplitude *= 0.5
                frequency *= 2
            altitude = map_value(altitude, -1, 1, MIN_ALTITUDE, MAX_ALTITUDE)
            for y in range(WORLD_HEIGHT):

                if y > altitude:
                    terrain.putpixel((x, y), TERRAIN_COLOR)
                else:
                    terrain.putpixel((x, y), SKY_COLOR)
        return terrain

    def draw_terrain(self):
        self.terrain_image = self.terrain_image.resize((WORLD_WIDTH * SCALE_FACTOR, WORLD_HEIGHT * SCALE_FACTOR), Image.NEAREST)
        self.terrain_tk_image = ImageTk.PhotoImage(self.terrain_image)
        self.ui.update_canvas(self.terrain_tk_image)

    def spawn_tanks(self):
        interval = WIDTH // (self.num_tanks + 1) # Calculate the interval to space tanks evenly
        spawn_positions = [i * interval for i in range(1, self.num_tanks + 1)]  # Generate positions
        spawn_positions[0] -= interval // 2
        spawn_positions[-1] += interval // 2
        self.tanks = []
        for i in range(self.num_tanks):
            tank_color = self.colors[i % len(self.colors)] # Cycle through colors if there are more tanks than colors
            tank = self.spawn_tank(spawn_positions[i], tank_color)
            self.tanks.append(tank)
        self.draw_tanks()

    def draw_tanks(self):
        for tank in self.tanks:
            tank.draw()
            self.ui.canvas.tag_raise(tank.id)
            self.ui.canvas.tag_raise(tank.turret)
            self.ui.canvas.tag_raise(tank.ui_text_id)

    def bind_controls(self):
        self.ui.bind_keys(self.control_power, self.move_turret, self.fire_projectile)

    def spawn_tank(self, spawn_x, color):
        base_altitude = 0
        # Adjust base altitude to ensure the tank is placed on the terrain
        while self.terrain_image.getpixel((spawn_x, base_altitude)) != TERRAIN_COLOR:
            base_altitude += 1 # The y-coordinate just above the terrain
        tank_y_position = int(base_altitude) - (TANK_SIZE // 2)

        # Clear space for the tank
        for x in range(spawn_x - TANK_SIZE // 2, spawn_x + TANK_SIZE // 2):
            for y in range(tank_y_position, int(base_altitude)):
                if 0 <= x < self.terrain_image.width and 0 <= y < self.terrain_image.height:
                    self.terrain_image.putpixel((x, y), TERRAIN_COLOR)
        return Tank(Pos(spawn_x, tank_y_position), color, self.ui.canvas)

    def control_power(self, dir):
        # Control the power of the tank's shot
        self.tanks[self.current_player].update_power(dir * 10)
        self.tanks[self.current_player].update_ui()

    def move_turret(self, dir):
        # Rotate the tank's turret
        self.tanks[self.current_player].rotate_turret(dir * 5)
        self.tanks[self.current_player].update_ui()

    def fire_projectile(self):
        # Fire a projectile from the current tank
        if not self.projectile_active and self.num_tanks > 1:
            #set initial horizontal and vertical velocities
            velx = self.tanks[self.current_player].power * math.cos(math.radians(self.tanks[self.current_player].angle))
            vely = -self.tanks[self.current_player].power * math.sin(math.radians(self.tanks[self.current_player].angle))
            p = Projectile(Pos(self.tanks[self.current_player].turret_end.x, self.tanks[self.current_player].turret_end.y - TANK_SIZE),
                           Pos(velx, vely), self.tanks[self.current_player].color, CRATER_SIZE, self.ui.canvas)
            self.trajectory_points = [(p.pos.x, p.pos.y)] # Initialize the trajectory points list
            self.projectile_active = True
            self.tanks[self.current_player].shots += 1 # update number of shots
            self.animate_projectile(p)

    def animate_projectile(self, projectile):
        gravity = 9.8 # Acceleration due to gravity
        time_interval = .05 # Time step for the simulation
        # Update horizontal position
        projectile.pos.x += projectile.vel.x * time_interval
        # Update vertical position
        projectile.pos.y += projectile.vel.y * time_interval + 0.5 * gravity * (time_interval ** 2)
        # Update vertical velocity
        projectile.vel.y += gravity * time_interval
        # Update projectile position on canvas
        self.ui.canvas.coords(projectile.projectile, projectile.pos.x - projectile.ball_size,
                              projectile.pos.y - projectile.ball_size,
                              projectile.pos.x + projectile.ball_size, projectile.pos.y + projectile.ball_size)
        # Append the new position to the trajectory points list
        self.trajectory_points.append((projectile.pos.x, projectile.pos.y))
        # Draw the trajectory line
        if len(self.trajectory_points) > 1:
            self.ui.canvas.create_line(self.trajectory_points[-2], self.trajectory_points[-1], fill=projectile.color,
                                       width=2, tags="line")
        if not (0 < projectile.pos.x < (WORLD_WIDTH * SCALE_FACTOR)):
            projectile.vel.x *= -1
        elif not (0 < projectile.pos.y < (WORLD_HEIGHT * SCALE_FACTOR)):
            projectile.vel.y *= -1
        elif self.check_collision(projectile):
            self.create_crater(projectile.pos.x, projectile.pos.y, projectile.explosion_radius)
            self.ui.canvas.delete("line")
            self.ui.canvas.delete(projectile.projectile)
            self.projectile_active = False
            self.end_turn()
            return
        self.ui.canvas.after(int(time_interval * 100), self.animate_projectile, projectile)

    def check_collision(self, projectile):
        if self.terrain_image.getpixel((projectile.pos.x, projectile.pos.y)) == TERRAIN_COLOR:
            return True
        return False

    def create_crater(self, x, y, radius):
        draw = ImageDraw.Draw(self.terrain_image)
        # Draw a filled circle to simulate the crater, filling it with sky color
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=SKY_COLOR)
        for i, tank in enumerate(self.tanks):
            if x - radius <= tank.pos.x <= x + radius and y - radius <= tank.pos.y <= y + radius:
                tank.lives -= 1
                if i != self.current_player:
                    shots = self.tanks[self.current_player].shots
                    # if tank managed to hit an opponent on nth attempt, aims to award accuracy
                    if shots == 1:
                        self.tanks[self.current_player].score += 50
                    elif shots == 2:
                        self.tanks[self.current_player].score += 25
                    else:
                        self.tanks[self.current_player].score += 10
            if tank.lives == 0:
                self.tanks.remove(tank)
                self.num_tanks -= 1
                self.ui.canvas.delete(tank.id)
                self.ui.canvas.delete(tank.turret)
                self.ui.canvas.delete(tank.ui_text_id)
        self.update_canvas()
        for tank in self.tanks:
            self.drop_tanks(tank)
        if len(self.tanks) == 1:
            self.tanks[-1].score += 10
            self.ui.show_winner_input(self.submit_winner_name)

    def submit_winner_name(self, name, dialog):
        # Submit the winner's name and update the hall of fame
        self.ui.display_winner(name, self.tanks[-1].color)
        dialog.destroy()
        self.hol.update(name, self.tanks[-1].score)
        with open("hall_of_fame_record.pkl", "wb") as file:
            pickle.dump(self.hol, file)

    def drop_tanks(self, tank):
        x = tank.pos.x
        y = tank.pos.y + 1
        if y == HEIGHT:
            tank.lives = 0
            self.tanks.remove(tank)
        elif self.terrain_image.getpixel((x, y)) != TERRAIN_COLOR:
            tank.update_tank(Pos(x, y))
            self.ui.canvas.after(int(.05 * 100), self.drop_tanks, tank)

    def update_canvas(self):
        self.tk_image = ImageTk.PhotoImage(self.terrain_image)
        self.ui.canvas.itemconfigure(tagOrId="terrain", image=self.tk_image)
        for tank in self.tanks:
            tank.draw()
    def end_turn(self):
        # End the current player's turn and switch to the next player
        self.current_player = (self.current_player + 1) % len(self.tanks)
        self.tanks[self.current_player].update_ui()

if __name__ == "__main__":
    root = tk.Tk()
    app = ScorchedEarth(root)
    root.mainloop()
