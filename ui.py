# ===== IMPORTS =====
# Import tkinter for creating the GUI window and canvas
from tkinter import *
import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk

# Import the game logic module (allows access to board state and turn info)
import importlib

from connect4_logic import check_win, moving_pieces
connect4_logic = importlib.import_module("connect4_logic")

# ===== GLOBAL VARIABLES =====
# These track the grid's position and size on the canvas
# They're updated whenever the window is resized
grid_start_x = 0      # Left edge of the grid (x-coordinate)
grid_start_y = 120    # Top edge of the grid (y-coordinate, below the title text)
cell_width = 0        # Width of each cell in pixels
cell_height = 0       # Height of each cell in pixels
center_x=0          # Center x-coordinate of the canvas (used for centering elements)
center_y=0          # Center y-coordinate of the canvas (used for centering elements)

# Global variable for the reset button
reset_button = None

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

# ===== RESET FUNCTION =====
def reset_game():
    """
    Resets the game to its initial state.
    Clears the board, resets the turn to player 1, and removes any win messages and reset button.
    """
    global reset_button
    # Reset the board
    connect4_logic.board = connect4_logic.create_board()
    # Reset turn to player 1
    connect4_logic.turn = 1
    # Clear any win messages from the canvas
    canvas.delete("win_message")
    # Remove the reset button if it exists
    if reset_button is not None:
        try:
            reset_button.destroy()
        except:
            pass  # Button might already be destroyed
        reset_button = None
    # Also try to destroy any remaining reset buttons that might exist
    for widget in root.winfo_children():
        if isinstance(widget, tk.Button) and widget.cget("text") == "Reset Game":
            try:
                widget.destroy()
            except:
                pass
    # Redraw the empty board
    draw_pieces()

# ===== WINDOW SETUP =====
# Create the main game window
root = tk.Tk()

# Create a canvas that will display the game (stretches to fill the window)
canvas = tk.Canvas(root, bg="white")
canvas.pack(fill="both", expand=True)

# ===== BACKGROUND IMAGE =====
# Load the background image file from assets
bg_image = tk.PhotoImage(file="assets/images/paper.png")

# Display the background image on the canvas
image_id = canvas.create_image(0, 0, image=bg_image, anchor="center")

# ===== TITLE TEXT =====
# Create the "Connect 4" title text 
text_id = canvas.create_text(0, 0, text="Connect 4", font=("Freestyle Script", 64), fill="#292929", anchor="n")

# ===== LOAD & CONVERT PIECE IMAGES =====
# Load and convert PIL images to PhotoImage for tkinter display
cookie = Image.open('assets/images/cookie.png')
cookie_resized = cookie.resize((130, 130))
player1_piece = ImageTk.PhotoImage(cookie_resized)

button = Image.open('assets/images/button.png')
button_resized = button.resize((130, 130))
player2_piece = ImageTk.PhotoImage(button_resized)



# ===== EVENT BINDINGS  =====
# Bind the window resize event - whenever the window is resized, resize_image() is called
canvas.bind("<Configure>", resize_image)




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
                
                #TODO: make the pieces drop down into place instead of just appearing in the final position
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
    Fins the column clicked and places the current player's piece in the lowest available row of that column.
    Does not allow placing pieces outside the grid and switches turns after a successful move.
    """
    # Calculate which column the click corresponds to based on x-coordinate
    col = (event.x - grid_start_x) // cell_width
    
    # Validate that the click was within the grid (columns 0-6)
    if col < 0 or col >= 7:
        return  # Ignore clicks outside the grid
    
    # Try to place the piece into the chosen column via game logic (lowest empty row)
    placed = moving_pieces(col, connect4_logic.turn)
    if not placed:
        return  # column full; ignore click

    # Redraw the board to show the newly placed piece
    draw_pieces()

    # Switch to the other player's turn only after a valid move
    if connect4_logic.turn == 1:
        connect4_logic.turn = 2
    else:
        connect4_logic.turn = 1

    # Check win after the move and display message if needed 
    #check if game is over. If it is, display a message.
    if(check_win(1)):
        # Get canvas dimensions for centering
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        
        # Define rectangle dimensions
        rect_width = 400
        rect_height = 100
        
        # Calculate rectangle position (centered)
        rect_x1 = (width - rect_width) // 2
        rect_y1 = (height - rect_height) // 2
        rect_x2 = rect_x1 + rect_width
        rect_y2 = rect_y1 + rect_height
        
        # Draw centered rectangle background
        canvas.create_rectangle(rect_x1, rect_y1, rect_x2, rect_y2, fill="white", outline="#292929", width=3, tags="win_message")
        
        # Draw win text centered in the rectangle
        text_x = width // 2
        text_y = height // 2
        canvas.create_text(text_x, text_y, text="Player 1 wins!", font=("Freestyle Script", 48), fill="#292929", anchor="center", tags="win_message")
        
        # Remove any existing reset buttons first
        for widget in root.winfo_children():
            if isinstance(widget, tk.Button) and widget.cget("text") == "Reset Game":
                try:
                    widget.destroy()
                except:
                    pass
        # Create reset button below the rectangle
        reset_button = tk.Button(root, text="Reset Game", command=reset_game, font=("Freestyle Script", 16), bg="#f0f0f0", fg="#292929")
        reset_button.place(relx=0.5, rely=0.7, anchor="center")
    elif(check_win(2)):
        # Get canvas dimensions for centering
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        
        # Define rectangle dimensions
        rect_width = 400
        rect_height = 100
        
        # Calculate rectangle position (centered)
        rect_x1 = (width - rect_width) // 2
        rect_y1 = (height - rect_height) // 2
        rect_x2 = rect_x1 + rect_width
        rect_y2 = rect_y1 + rect_height
        
        # Draw centered rectangle background
        canvas.create_rectangle(rect_x1, rect_y1, rect_x2, rect_y2, fill="white", outline="#292929", width=3, tags="win_message")
        
        # Draw win text centered in the rectangle
        text_x = width // 2
        text_y = height // 2
        canvas.create_text(text_x, text_y, text="Player 2 wins!", font=("Freestyle Script", 48), fill="#292929", anchor="center", tags="win_message")
        
        # Remove any existing reset buttons first
        for widget in root.winfo_children():
            if isinstance(widget, tk.Button) and widget.cget("text") == "Reset Game":
                try:
                    widget.destroy()
                except:
                    pass
        # Create reset button below the rectangle
        reset_button = tk.Button(root, text="Reset Game", command=reset_game, font=("Freestyle Script", 16), bg="#f0f0f0", fg="#292929")
        reset_button.place(relx=0.5, rely=0.7, anchor="center")

# Bind the mouse click event - whenever the canvas is clicked, on_canvas_click() is called
canvas.bind("<Button-1>", on_canvas_click)


# ===== START THE GAME =====
# Begin the main event loop (keeps the window open and responsive to user input)
root.mainloop()

