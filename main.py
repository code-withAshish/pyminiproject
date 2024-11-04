import os
import tkinter as tk
import random
import csv
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd


def load_last_game_number():
    """Load the last game number from the CSV file."""
    filename = "game_data.csv"
    if os.path.exists(filename):
        try:
            data = pd.read_csv(filename)
            return data["Game Number"].max() if not data.empty else 0
        except Exception as e:
            print(f"Error loading game data: {e}")
    return 0


class Tile:
    """Class to represent a single tile in the game."""
    def __init__(self, number):
        self.number = number
        self.revealed = False


class TileGame:
    game_number = load_last_game_number() + 1  # Increment from the last game number

    def __init__(self, root, grid_size=4):
        self.root = root
        self.grid_size = grid_size
        self.tiles = []
        self.first_click = None
        self.second_click = None
        self.matched_pairs = 0
        self.time_elapsed = 0
        self.timer_running = False

        self.timer_label = tk.Label(self.root, text="Time: 0 sec", font=("Arial", 14))
        self.timer_label.grid(row=grid_size + 1, column=1, columnspan=grid_size, pady=10)

        self.create_tiles()
        self.update_timer()

    def create_tiles(self):
        """Create and shuffle the tiles for the game."""
        numbers = list(range(1, (self.grid_size ** 2) // 2 + 1)) * 2
        random.shuffle(numbers)

        for _ in range(self.grid_size):
            row_tiles = [Tile(numbers.pop()) for _ in range(self.grid_size)]
            self.tiles.append(row_tiles)
            for col, tile in enumerate(row_tiles):
                button = tk.Button(self.root, text="", width=10, height=5,
                                   command=lambda r=len(self.tiles) - 1, c=col: self.on_click(r, c))
                button.grid(row=len(self.tiles) - 1, column=col, padx=5, pady=5)
                tile.button = button  # Link button to the tile

    def on_click(self, row, col):
        """Handle tile click events."""
        if not self.timer_running:
            self.timer_running = True
        tile = self.tiles[row][col]
        if tile.revealed or self.second_click:
            return

        self.first_click = self.first_click or (row, col)
        self.reveal_tile(tile)
        if self.first_click and self.first_click != (row, col):
            self.second_click = (row, col)
            self.root.after(1000, self.check_match)

    def reveal_tile(self, tile):
        """Reveal a tile by updating the button display."""
        tile.button.config(text=str(tile.number))
        tile.revealed = True

    def hide_tile(self, row, col):
        """Hide a tile by resetting the button display."""
        tile = self.tiles[row][col]
        tile.button.config(text="")
        tile.revealed = False

    def check_match(self):
        """Check if the two revealed tiles match."""
        r1, c1 = self.first_click
        r2, c2 = self.second_click
        if self.tiles[r1][c1].number == self.tiles[r2][c2].number:
            self.matched_pairs += 1
        else:
            self.hide_tile(r1, c1)
            self.hide_tile(r2, c2)

        self.first_click = None
        self.second_click = None

        if self.matched_pairs == (self.grid_size ** 2) // 2:
            self.end_game()

    def update_timer(self):
        """Update the timer display."""
        if self.timer_running:
            self.time_elapsed += 1
            self.timer_label.config(text=f"Time: {self.time_elapsed} sec")
        self.root.after(1000, self.update_timer)

    def end_game(self):
        """Handle end-of-game logic."""
        self.timer_running = False
        self.clear_grid()
        tk.Label(self.root, text=f"You completed the game in {self.time_elapsed} seconds!", font=("Arial", 16)).grid(
            row=1, column=1, columnspan=3, pady=20)
        tk.Button(self.root, text="See Stats", command=self.show_stats, font=("Arial", 14)).grid(row=2, column=1, columnspan=3)
        self.save_game_data()

    def clear_grid(self):
        """Clear the grid of buttons."""
        for widget in self.root.winfo_children():
            widget.grid_forget()

    def save_game_data(self):
        """Save game data to a CSV file."""
        filename = "game_data.csv"
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            with open(filename, mode="a", newline="") as file:
                writer = csv.writer(file)
                if file.tell() == 0:
                    writer.writerow(["Game Number", "Time Taken (seconds)", "Grid Size", "Date & Time"])
                writer.writerow([TileGame.game_number, self.time_elapsed, self.grid_size, now])
        except Exception as e:
            print(f"Error saving game data: {e}")

    def show_stats(self):
        """Display the game statistics."""
        self.clear_grid()
        try:
            data = pd.read_csv("game_data.csv")
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.plot(data["Game Number"], data["Time Taken (seconds)"], marker='o')
            ax.set_title("Game Completion Time")
            ax.set_xlabel("Game Number")
            ax.set_ylabel("Time Taken (seconds)")
            ax.grid(True)

            canvas = FigureCanvasTkAgg(fig, master=self.root)
            canvas.draw()
            canvas.get_tk_widget().grid(row=0, column=0, columnspan=4)

            tk.Button(self.root, text="Back to Game", command=self.start_new_game).grid(row=1, column=0, columnspan=4, pady=20)
        except Exception as e:
            tk.messagebox.showerror("Error", f"Could not load stats: {e}")

    def start_new_game(self):
        """Start a new game."""
        self.clear_grid()
        self.matched_pairs = 0
        self.time_elapsed = 0
        self.first_click = None
        self.second_click = None
        self.timer_running = False
        self.create_tiles()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Tile Matching Game")
    game = TileGame(root)
    root.mainloop()
