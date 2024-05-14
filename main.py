import tkinter as tk
import random
import math

class Player:
    def __init__(self, canvas, x, terrain_points):
        self.canvas = canvas
        self.x = x
        self.y = self.get_y_from_terrain(x, terrain_points)
        self.angle = 45
        self.power = 50
        self.avatar = canvas.create_oval(x - 10, self.y - 10, x + 10, self.y + 10, fill='red')

    def get_y_from_terrain(self, x, terrain_points):
        # Find the closest points on either side and interpolate the y-coordinate
        for i in range(len(terrain_points) - 1):
            if terrain_points[i][0] <= x <= terrain_points[i + 1][0]:
                x1, y1 = terrain_points[i]
                x2, y2 = terrain_points[i + 1]
                # Linear interpolation
                y = y1 + (y2 - y1) * ((x - x1) / (x2 - x1))
                return y
        return self.canvas.winfo_height()
    def update_display(self, angle_label, power_label):
        angle_label.config(text=f"Angle: {self.angle}")
        power_label.config(text=f"Power: {self.power}")

class ScorchedEarthGame:
    def __init__(self, root):
        self.root = root
        self.width = 800
        self.height = 400
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg='sky blue')
        self.canvas.pack()
        self.setup_game()

    def setup_game(self):

        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(pady=20)
        self.num_players_label = tk.Label(self.input_frame, text="Enter number of players:")
        self.num_players_label.pack(side=tk.LEFT)
        self.num_players_entry = tk.Entry(self.input_frame)
        self.num_players_entry.pack(side=tk.LEFT)
        self.start_button = tk.Button(self.input_frame, text="Start Game", command=self.start_game)
        self.start_button.pack(side=tk.LEFT)

    def start_game(self):
        try:
            self.num_players = int(self.num_players_entry.get())
            self.input_frame.destroy()
            self.initialize_game()
        except ValueError:
            self.num_players_label.config(text="Enter a valid number:")

    def initialize_game(self):
        self.terrain_points = self.generate_terrain()
        self.draw_terrain(self.terrain_points)
        self.setup_controls()
        player_x = random.randint(50, self.width - 50)
        self.players = [Player(self.canvas, player_x, self.terrain_points)]
        self.current_player = self.players[0]
        self.current_player.update_display(self.angle_label, self.power_label)

    def generate_terrain(self):
        points = [(0, self.height)]
        for i in range(1, 100):
            x = i * (self.width // 50)
            y = random.randint(self.height // 2, self.height - 10)
            points.append((x, y))
        points.append((self.width, self.height))
        return points

    def draw_terrain(self, points):
        # Draw the terrain
        self.canvas.delete('terrain')
        self.canvas.create_polygon(points + [(self.width, self.height), (0, self.height)], fill='saddle brown',
                                   tag='terrain')

    def setup_controls(self):
        self.angle_label = tk.Label(self.root, text="Angle: 45")
        self.angle_label.pack()
        self.power_label = tk.Label(self.root, text="Power: 50")
        self.power_label.pack()
        self.root.bind('<Left>', self.decrease_angle)
        self.root.bind('<Right>', self.increase_angle)
        self.root.bind('<Up>', self.increase_power)
        self.root.bind('<Down>', self.decrease_power)
        self.root.bind('<space>', self.fire_projectile)
        self.fire_button = tk.Button(self.root, text="Fire!", command=self.fire_projectile)
        self.fire_button.pack()
    def increase_angle(self, event):
        self.current_player.angle = (self.current_player.angle + 5) % 360
        self.angle_label.config(text=f"Angle: {self.current_player.angle}")

    def decrease_angle(self, event):
        self.current_player.angle = (self.current_player.angle - 5) % 360
        self.angle_label.config(text=f"Angle: {self.current_player.angle}")

    def increase_power(self, event):
        self.current_player.power = min(self.current_player.power + 5, 100)
        self.power_label.config(text=f"Power: {self.current_player.power}")

    def decrease_power(self, event):
        self.current_player.power = max(self.current_player.power - 5, 0)
        self.power_label.config(text=f"Power: {self.current_player.power}")

    def fire_projectile(self):
        start_x = self.current_player.x
        start_y = self.current_player.y - 10  # Adjusted for visual positioning
        angle_rad = math.radians(self.current_player.angle)
        velocity_x = self.current_player.power * math.cos(angle_rad)
        velocity_y = -self.current_player.power * math.sin(angle_rad)

        # Create the projectile object on the canvas
        projectile = self.canvas.create_oval(start_x - 5, start_y - 5, start_x + 5, start_y + 5, fill='red',
                                             tag='projectile')

        # Start animating the projectile
        self.animate_projectile(start_x, start_y, velocity_x, velocity_y, projectile)

    def animate_projectile(self, x, y, vel_x, vel_y, projectile):
        gravity = 0.98
        time_interval = 0.05
        x += vel_x * time_interval
        y += vel_y * time_interval + 0.5 * gravity * time_interval ** 2
        vel_y += gravity * time_interval

        # Update projectile position
        self.canvas.coords(projectile, x - 5, y - 5, x + 5, y + 5)

        # Check for conditions to stop and remove the projectile
        if self.check_collision_with_terrain(x, y):
            self.canvas.delete(projectile)  # Remove the projectile from the canvas
            self.create_crater(x, y)
        elif not self.is_within_canvas(x, y):
            self.canvas.delete(projectile)  # Remove if out of bounds
        else:
            # Continue the animation if no collision and still within bounds
            self.root.after(int(time_interval * 1000), self.animate_projectile, x, y, vel_x, vel_y, projectile)

    def create_crater(self, impact_x, impact_y):
        crater_radius = 20  # Define the radius of the crater
        crater_depth = 10  # Define how deep the crater goes

        for i in range(len(self.terrain_points)):
            x, y = self.terrain_points[i]
            distance = math.sqrt((x - impact_x) ** 2 + (y - impact_y) ** 2)
            if distance < crater_radius:
                # Adjust y-coordinate to create a crater effect
                self.terrain_points[i] = (x, y + crater_depth * (1 - distance / crater_radius))

        # Redraw the terrain with the crater
        self.draw_terrain(self.terrain_points)

    def check_collision_with_terrain(self, x, y):
        # Implement collision detection with terrain
        for (px, py) in self.terrain_points:
            if abs(px - x) < 5 and y >= py:
                return True
        return False

    def is_within_canvas(self, x, y):
        # Check if the projectile is still within the visible area of the canvas
        return 0 <= x <= self.width and 0 <= y <= self.height


def main():
    root = tk.Tk()
    root.title("Scorched Earth Game")
    game = ScorchedEarthGame(root)
    root.mainloop()

# Uncomment the next line to start the game
main()
