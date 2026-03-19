# ===== IMPORTS =====
# Import tkinter for creating the GUI window and canvas
from tkinter import *
import tkinter as tk
from tkinter import font

# Import the game logic module (allows access to board state and turn info)
import importlib
connect4_logic = importlib.import_module("connect4_logic")

# ===== GLOBAL VARIABLES =====
# These track the grid's position and size on the canvas
# They're updated whenever the window is resized
grid_start_x = 0      # Left edge of the grid (x-coordinate)
grid_start_y = 120    # Top edge of the grid (y-coordinate, below the title text)
cell_width = 0        # Width of each cell in pixels
cell_height = 0       # Height of each cell in pixels

# ===== RESIZE EVENT HANDLER =====
def resize_image(event):
    """Called whenever the window is resized. Updates all game elements to fit the new size."""
    global grid_start_x, grid_start_y, cell_width, cell_height
    
    # Update canvas size to match the new window dimensions
    canvas.config(width=event.width, height=event.height)
    
    # Reposition the background image in the center of the canvas
    canvas.coords(image_id, event.width // 2, event.height // 2)
    
    # Keep the "Connect 4" title text at the top center
    canvas.coords(text_id, event.width // 2, 20)

    # Recalculate grid dimensions and redraw grid lines
    draw_grid(event.width, event.height, grid_start_y=120)
    
    # Redraw all pieces on the board in their new positions
    draw_pieces()

# ===== GRID DRAWING FUNCTION =====
def draw_grid(width, height, grid_start_y=120):
    """
    Draws the Connect 4 grid lines on the canvas.
    
    The grid is centered horizontally and starts at grid_start_y pixels from the top.
    Grid cells are kept roughly square (not stretched into rectangles).
    """
    global grid_start_x, cell_width, cell_height
    
    # Remove all previous grid lines from the canvas
    canvas.delete("grid_line")

    # Calculate cell dimensions to make the grid more square
    # Cell height is based on available vertical space (total height minus text area, divided by 6 rows)
    cell_height = (height - grid_start_y) // 6
    # Cell width matches cell height to create square cells
    cell_width = cell_height
    # Total width needed for all 7 columns
    grid_width = 7 * cell_width
    # Center the grid horizontally on the canvas
    grid_start_x = (width - grid_width) // 2

    # Draw vertical lines (these separate the 7 columns)
    for col in range(1, 7):
        x = grid_start_x + col * cell_width
        canvas.create_line(x, grid_start_y, x, height, fill="#292929", tags="grid_line")

    # Draw horizontal lines (these separate the 6 rows)
    for row in range(1, 6):
        y = grid_start_y + row * cell_height
        canvas.create_line(grid_start_x, y, grid_start_x + grid_width, y, fill="#292929", tags="grid_line")

# ===== WINDOW SETUP =====
# Create the main game window
root = tk.Tk()

# Create a canvas that will display the game (stretches to fill the window)
canvas = tk.Canvas(root, bg="white")
canvas.pack(fill="both", expand=True)

# ===== BACKGROUND IMAGE =====
# Load the background image file from assets
bg_image = tk.PhotoImage(file="assets/images/paper.png")

# Display the background image on the canvas (centered)
image_id = canvas.create_image(0, 0, image=bg_image, anchor="center")

# ===== TITLE TEXT =====
# Create the "Connect 4" title text (positioned at top center)
text_id = canvas.create_text(0, 0, text="Connect 4", font=("Freestyle Script", 64), fill="#292929", anchor="n")

# ===== EVENT BINDINGS  =====
# Bind the window resize event - whenever the window is resized, resize_image() is called
canvas.bind("<Configure>", resize_image)

# ===== PIECE IMAGES =====
# Load images for player pieces from assets folder
player1_piece = tk.PhotoImage(file="assets/images/cookie.png")  # Player 1's piece (cookie)
player2_piece = tk.PhotoImage(file="assets/images/button.png")  # Player 2's piece (button)

# ===== PIECE DRAWING FUNCTION =====
def draw_pieces():
    """
    Draws all pieces currently on the board.
    This function reads the board array from connect4_logic
    and displays the appropriate piece image for each position.
    """
    # Remove all previously drawn pieces from the canvas
    canvas.delete("pieces")
    
    # Loop through every position on the 6 rows x 7 columns board
    for row in range(6):
        for col in range(7):
            # Only draw a piece if there's something at this position (0 = empty)
            if connect4_logic.board[row][col] != 0:
                # Calculate the pixel coordinates for the center of this grid cell
                x = grid_start_x + (col * cell_width) + (cell_width // 2)
                y = grid_start_y + (row * cell_height) + (cell_height // 2)
                
                # Draw Player 1's piece (board value = 1)
                if connect4_logic.board[row][col] == 1:
                    canvas.create_image(x, y, image=player1_piece, tags="pieces")
                # Draw Player 2's piece (board value = 2)
                elif connect4_logic.board[row][col] == 2:
                    canvas.create_image(x, y, image=player2_piece, tags="pieces")

# ===== CLICK EVENT HANDLER =====
def on_canvas_click(event):
    """
    Called when the player clicks on the canvas.
    Determines which column was clicked, finds the lowest available row,
    and drops a piece there. Then switches to the other player's turn.
    """
    # Calculate which column the click corresponds to based on x-coordinate
    col = (event.x - grid_start_x) // cell_width
    
    # Validate that the click was within the grid (columns 0-6)
    if col < 0 or col >= 7:
        return  # Ignore clicks outside the grid
    
    # Find the lowest (highest row number) empty cell in the selected column
    # Start from row 5 (bottom) and go backwards to row 0 (top)
    for row in range(5, -1, -1):
        if connect4_logic.board[row][col] == 0:  # Found an empty spot
            # Place the current player's piece (1 or 2)
            connect4_logic.board[row][col] = connect4_logic.turn
            
            # Switch to the other player's turn
            if connect4_logic.turn == 1:
                connect4_logic.turn = 2
            else:
                connect4_logic.turn = 1
            
            # Redraw the board to show the newly placed piece
            draw_pieces()
            break  # Stop searching after placing the piece

# Bind the mouse click event - whenever the canvas is clicked, on_canvas_click() is called
canvas.bind("<Button-1>", on_canvas_click)

# ===== START THE GAME =====
# Begin the main event loop (keeps the window open and responsive to user input)
root.mainloop()

