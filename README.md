# Sudoku-Solver
Python sudoku solver using pygame for the window and visual representation of the process

# August 30, 2020
Now a full functioning sudoku application.

# Features
- "Generate Grid" generate grids for the user to solve
    - the numbers of the loaded grid will appear in yellow, and cannot manually changed by the user
- "Check" highlights any conflicts in red
- "Solve" solves any grid if the grid is solvable, else displays a message saying it cannot be solved
- "Load Hardest" loads what is considered the hardest sudoku grid in the world
- "Show Possible" toggles what numbers are possible where
- "Clear" loads a blank grid

# Other
- entering a number on a filled grid will clear the grid, instead of replacing it
- The grey square indicates a selected cell
    - Clicking on a cell will select it
    - ESC will deselect the cell
    - Arrow Keys move the grey square
