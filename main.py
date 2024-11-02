import tkinter as tk
import random
import csv
from datetime import datetime
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd


class TileGame:
    def __init__(self, root, grid_size=4):
        """
        Initialize the game with a grid of hidden tiles, a timer, and matched-pair tracking.

        Args:
            root: The main Tkinter window.
            grid_size: The size of the grid (default 4x4).
        """
        self.root = root
        self.grid_size = grid_size
        self.tiles = []  # Stores all tiles with button and number information
        self.first_click = None  # To track the first tile clicked
        self.second_click = None  # To track the second tile clicked
        self.matched_pairs = 0  # Track the number of matched pairs

        # Set up the tiles and timer
        self.create_tiles()

        # Timer setup
        self.timer_label = tk.Label(self.root, text="Time: 0 sec", font=("Arial", 14))
        self.timer_label.grid(row=grid_size + 1, column=1, columnspan=grid_size, pady=10)
        self.time_elapsed = 0  # Timer starts from 0
        self.timer_running = False  # Control when the timer starts
        self.update_timer()  # Start the timer update loop

    def create_tiles(self):
        """
        Create a grid of buttons representing tiles with hidden numbers,
        and center the grid within the window.
        """
        # Generate a list of number pairs for the tiles and shuffle them
        numbers = list(range(1, (self.grid_size ** 2) // 2 + 1)) * 2
        random.shuffle(numbers)  # Shuffle the number pairs randomly

        # Create and place each button (tile) in the grid
        for row in range(1, self.grid_size + 1):
            row_tiles = []  # Store tiles for the current row
            for col in range(1, self.grid_size + 1):
                number = numbers.pop()  # Assign a number to this tile
                # Create a button for the tile that triggers on_click when clicked
                button = tk.Button(self.root, text="", width=10, height=5,
                                   command=lambda r=row, c=col: self.on_click(r - 1, c - 1))
                button.grid(row=row, column=col, padx=5, pady=5)  # Place the button in the grid
                # Store each tile with its button, number, and revealed status
                row_tiles.append({"button": button, "number": number, "revealed": False})
            self.tiles.append(row_tiles)  # Add the row of tiles to the main tile list

    def on_click(self, row, col):
        """
        Handle the click on a tile: reveal the tile, track clicks,
        and check for matches if two tiles are clicked.

        Args:
            row: The row index of the clicked tile.
            col: The column index of the clicked tile.
        """
        # Start the timer on the first tile click
        if not self.timer_running:
            self.timer_running = True

        tile = self.tiles[row][col]  # Get the clicked tile
        if tile["revealed"]:
            return  # Ignore clicks on already revealed tiles

        # Track the first and second clicks
        if not self.first_click:
            self.first_click = (row, col)  # Store the position of the first click
            self.reveal_tile(row, col)  # Reveal the tile
        elif not self.second_click:
            self.second_click = (row, col)  # Store the position of the second click
            self.reveal_tile(row, col)  # Reveal the second tile
            # After both tiles are clicked, check for a match after a short delay
            self.root.after(1000, self.check_match)
        else:
            return  # Ignore any additional clicks while waiting for match check

    def reveal_tile(self, row, col):
        """
        Show the number on a tile and set its status to revealed.

        Args:
            row: The row index of the tile.
            col: The column index of the tile.
        """
        tile = self.tiles[row][col]  # Access the specific tile
        tile["button"].config(text=str(tile["number"]))  # Update the button text to show the number
        tile["revealed"] = True  # Mark the tile as revealed

    def hide_tile(self, row, col):
        """
        Hide the number on a tile and reset its revealed status.

        Args:
            row: The row index of the tile.
            col: The column index of the tile.
        """
        tile = self.tiles[row][col]  # Access the specific tile
        tile["button"].config(text="")  # Clear the button text to hide the number
        tile["revealed"] = False  # Mark the tile as not revealed

    def check_match(self):
        """
        Check if the two revealed tiles match. If they match, leave them revealed;
        if they don’t match, hide both tiles. Also check if all pairs are matched
        to end the game.
        """
        r1, c1 = self.first_click  # Get the first click coordinates
        r2, c2 = self.second_click  # Get the second click coordinates

        # Check if the two selected tiles have the same number
        if self.tiles[r1][c1]["number"] == self.tiles[r2][c2]["number"]:
            # It's a match! Increase matched pairs count
            self.matched_pairs += 1
        else:
            # Not a match, hide both tiles
            self.hide_tile(r1, c1)
            self.hide_tile(r2, c2)

        # Reset click tracking for the next turn
        self.first_click = None
        self.second_click = None

        # Check if all pairs have been matched
        if self.matched_pairs == (self.grid_size ** 2) // 2:
            self.end_game()  # End the game if all pairs are matched

    def update_timer(self):
        """
        Update the timer label every second if the timer is running.
        """
        if self.timer_running:
            self.time_elapsed += 1  # Increment the elapsed time
            self.timer_label.config(text=f"Time: {self.time_elapsed} sec")  # Update the timer display

        # Continue updating the timer every second
        self.root.after(1000, self.update_timer)

    def end_game(self):
        """
        Display a winner message and stop the timer once all pairs are matched.
        Save the game data to a CSV file for later analysis.
        """
        self.timer_running = False  # Stop the timer
        self.clear_grid()  # Clear the game grid for the end message

        # Show the completion message and See Stats button
        tk.Label(self.root, text=f"You completed the game in {self.time_elapsed} seconds!", font=("Arial", 16)).grid(
            row=1, column=1, columnspan=3, pady=20)
        see_stats_button = tk.Button(self.root, text="See Stats", command=self.show_stats, font=("Arial", 14))
        see_stats_button.grid(row=2, column=1, columnspan=3)

        # Save game data to CSV file
        self.save_game_data()

    def clear_grid(self):
        """
        Clear all tile buttons from the screen.
        """
        for widget in self.root.winfo_children():  # Iterate over all widgets in the main window
            widget.grid_forget()  # Remove each widget from the grid

    def save_game_data(self):
        """
        Save game data to a CSV file with columns: Game Number, Time Taken, Grid Size, Date & Time.
        """
        filename = "game_data.csv"  # Define the filename for storing game data
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get the current date and time

        try:
            with open(filename, mode="a", newline="") as file:  # Open the file in append mode
                writer = csv.writer(file)  # Create a CSV writer object
                if file.tell() == 0:  # Check if the file is empty
                    writer.writerow(["Game Number", "Time Taken (seconds)", "Grid Size", "Date & Time"])  # Write headers
                game_number = self.matched_pairs  # Use matched pairs as the game number
                writer.writerow([game_number, self.time_elapsed, self.grid_size, now])  # Save the game data
        except Exception as e:
            print(f"Error saving game data: {e}")  # Print an error message if saving fails

    def show_stats(self):
        """
        Load game data from the CSV file and display stats using Matplotlib embedded in the Tkinter window.
        """
        self.clear_grid()  # Clear the current screen for stats

        # Load the data
        try:
            data = pd.read_csv("game_data.csv")  # Read the CSV file containing game data
            fig, ax = plt.subplots(figsize=(8, 4))  # Create a Matplotlib figure
            ax.plot(data["Game Number"], data["Time Taken (seconds)"], marker="o", linestyle='-')  # Plot data
            ax.set_title("Game Time vs. Game Number")  # Set plot title
            ax.set_xlabel("Game Number")  # Set x-axis label
            ax.set_ylabel("Time Taken (seconds)")  # Set y-axis label
            ax.grid(True)  # Show grid on the plot
            canvas = FigureCanvasTkAgg(fig, master=self.root)  # Create a canvas to display the plot in Tkinter
            canvas.draw()  # Draw the canvas
            canvas.get_tk_widget().grid(row=0, column=0, columnspan=4)  # Place the canvas in the grid
        except Exception as e:
            messagebox.showerror("Error", "Unable to load game stats. Please check if the game has been played.")  # Error message

# Main execution
if __name__ == "__main__":
    root = tk.Tk()  # Create the main Tkinter window
    root.title("Tile Matching Game")  # Set the window title
    game = TileGame(root)  # Initialize the game
    root.mainloop()  # Start the Tkinter event loop
