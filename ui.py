import tkinter as tk
from tkinter import NW
from util import *
class GameUI:
    def __init__(self, root, start_game_callback, show_hall_of_fame_callback, set_num_tanks_callback):
        self.root = root
        self.start_game_callback = start_game_callback
        self.show_hall_of_fame_callback = show_hall_of_fame_callback
        self.set_num_tanks_callback = set_num_tanks_callback
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
        self.canvas.pack()
        self.button_frame = tk.Frame(root)
        self.play_button = tk.Button(self.button_frame, text="Play", command=self.start_game, width=20, height=2)
        self.play_button.grid(row=0, column=0, padx=10, pady=10)
        self.hall_of_fame_button = tk.Button(self.button_frame, text="Hall of Fame", command=self.show_hall_of_fame, width=20, height=2)
        self.hall_of_fame_button.grid(row=1, column=0, padx=10, pady=10)
        self.scale_widget = tk.Scale(self.button_frame, from_=2, to=4, orient=tk.HORIZONTAL, command=self.set_num_tanks)
        self.scale_widget.set(2)
        self.scale_widget.grid(row=2, column=0, padx=10, pady=10)
        self.button_frame.place(relx=0.5, rely=0.5, anchor='center')

    def start_game(self):
        self.scale_widget.destroy()
        self.button_frame.destroy()
        self.canvas.pack()
        self.start_game_callback()

    def show_hall_of_fame(self):
        self.show_hall_of_fame_callback()

    def set_num_tanks(self, value):
        self.set_num_tanks_callback(int(value))

    def update_canvas(self, image):
        self.canvas.create_image(0, 0, anchor=NW, image=image, tags="terrain")

    def bind_keys(self, control_power, move_turret, fire_projectile):
        self.root.bind('<Up>', lambda event: control_power(1))
        self.root.bind('<Down>', lambda event: control_power(-1))
        self.root.bind('<Left>', lambda event: move_turret(1))
        self.root.bind('<Right>', lambda event: move_turret(-1))
        self.root.bind('<space>', lambda event: fire_projectile())

    def display_winner(self, winner_name, color):
        ui_text = f"{winner_name} ({color}) won"
        self.canvas.create_text(WORLD_WIDTH // 2 + 10, WORLD_HEIGHT // 2, text=ui_text, fill=color,
                                font=('Helvetica', '15', 'bold'), anchor='center')

    def show_winner_input(self, submit_callback):
        input_dialog = tk.Toplevel(self.root)
        input_dialog.title("Winner Name")
        tk.Label(input_dialog, text="Type your name:").pack(padx=10, pady=10)
        entry = tk.Entry(input_dialog)
        entry.pack(padx=10, pady=10)
        submit_button = tk.Button(input_dialog, text="Submit", command=lambda: submit_callback(entry.get(), input_dialog))
        submit_button.pack(padx=10, pady=10)
        input_dialog.geometry("+%d+%d" % (self.root.winfo_x() + self.root.winfo_width() // 2,
                                          self.root.winfo_y() + self.root.winfo_height() // 2))

