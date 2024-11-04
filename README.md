# Tile Matching Game

## Introduction

Welcome to the Tile Matching Game, a classic memory game that challenges players to match pairs of tiles. The game is designed to enhance cognitive skills, improve memory, and provide an engaging experience for players of all ages. In this game, players are presented with a grid of tiles that are initially hidden. The objective is to flip two tiles at a time, revealing their numbers, and find matching pairs. The game tracks the time taken to complete and records the statistics for future analysis.

## Features

- **Dynamic Tile Generation**: The game generates a grid of tiles based on a specified size (default is 4x4). Each tile has a number, and pairs are created randomly.
- **Timer Functionality**: The game includes a timer that tracks how long it takes to complete the game, promoting a fun challenge to improve performance.
- **Statistics Tracking**: Game statistics, including the game number, time taken, grid size, and the date/time of completion, are recorded in a CSV file. This allows players to track their progress over time.
- **Data Visualization**: Players can view their game statistics in a visual format, displaying completion times for each game. This feature utilizes data science techniques to provide insights into performance.

## Technologies Used

- **Python**: The primary programming language used for developing the game. Python's simplicity and readability make it an excellent choice for rapid development.
- **Tkinter**: The built-in GUI toolkit for Python used to create the game's graphical user interface. Tkinter provides an easy way to design windows, buttons, and other widgets, allowing for a responsive and interactive gaming experience.
- **Pandas**: A powerful data manipulation library that facilitates reading and writing game statistics to and from CSV files. It is used to handle game data effectively and provide data analysis capabilities.
- **Matplotlib**: A plotting library for Python used to visualize game statistics. It enables the display of graphs that represent player performance over multiple games, providing insights into improvements or trends.
