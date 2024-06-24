import math
from util import *
import projectile


class Tank:
    def __init__(self, pos: Pos, color, canvas, angle=90):
        self.canvas = canvas
        self.pos = pos
        self.color = color
        self.size = TANK_SIZE
        self.angle = angle
        self.turret_length = 6
        self.id = None
        self.turret = None
        self.turret_base = Pos(self.pos.x, self.pos.y - TANK_SIZE / 2)
        self.turret_end = Pos(*rotate(self.turret_base.x, self.turret_base.y, self.angle, self.turret_length))
        self.power = 0
        self.lives = 1
        self.shots = 0
        self.score = 0
        self.ui_text_id = None  # UI text ID for updating

    def draw(self):
        if self.id:
            self.canvas.delete(self.id)
        if self.turret:
            self.canvas.delete(self.turret)
        x1 = self.pos.x - self.size
        y1 = self.pos.y - self.size / 2
        x2 = self.pos.x + self.size
        y2 = self.pos.y + self.size / 2
        self.turret_end = Pos(*rotate(self.turret_base.x, self.turret_base.y, self.angle, self.turret_length))
        self.turret = self.canvas.create_line(self.turret_base.x, self.turret_base.y, self.turret_end.x, self.turret_end.y, fill=self.color, width=3)
        self.id = self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.color)
        self.draw_ui()

    def draw_ui(self):
        # Draw UI elements above the tank
        if self.ui_text_id:
            self.canvas.delete(self.ui_text_id)
        ui_text = f"Lives: {self.lives} Score: {self.score}\nAngle: {self.angle} Power: {self.power}"
        self.ui_text_id = self.canvas.create_text(self.pos.x, self.pos.y - 20, text=ui_text, fill=self.color, font=('Helvetica', '10', 'bold'), anchor='center')

    def update_ui(self):
        # Update the UI elements above the tank
        self.draw_ui()

    def rotate_turret(self, angle):
        if 0 <= self.angle + angle <= 180:
            self.angle += angle
            self.update_turret()

    def update_tank(self, tank_pos):
        self.pos = tank_pos
        self.turret_base = Pos(self.pos.x, self.pos.y - TANK_SIZE / 2)
        self.update_turret()
        x1 = self.pos.x - self.size
        y1 = self.pos.y - self.size / 2
        x2 = self.pos.x + self.size
        y2 = self.pos.y + self.size / 2
        self.canvas.coords(self.id, x1, y1, x2, y2)

    def update_turret(self):
        self.turret_end = Pos(*rotate(self.turret_base.x, self.turret_base.y, self.angle, self.turret_length))
        self.canvas.coords(self.turret, self.turret_base.x, self.turret_base.y, self.turret_end.x, self.turret_end.y)

    def update_power(self, power):
        if 0 <= self.power + power <= 100:
            self.power += power

    def fire_projectile(self):
        velx = self.power * math.cos(math.radians(self.angle))
        vely = -self.power * math.sin(math.radians(self.angle))
        p = projectile.Projectile(Pos(self.turret_end.x, self.turret_end.y - TANK_SIZE), Pos(velx, vely), self.color, 20, self.canvas)
        return p
