from tkinter import *
import tkinter as tk
from tkinter import font
import importlib
connect4_logic = importlib.import_module("connect4_logic")

# Global variables to track grid geometry
grid_start_x = 0
grid_start_y = 120
cell_width = 0
cell_height = 0

def resize_image(event):
    global grid_start_x, grid_start_y, cell_width, cell_height
    
    # Resize the canvas to match the window size
    canvas.config(width=event.width, height=event.height)
    # Redraw the image at the center of the canvas
    canvas.coords(image_id, event.width // 2, event.height // 2)
    # Keep the text at the top center
    canvas.coords(text_id, event.width // 2, 20)

    # Redraw the grid to fit the resized canvas (starting below the text)
    draw_grid(event.width, event.height, grid_start_y=120)
    
    # Redraw pieces after resizing
    draw_pieces()

def draw_grid(width, height, grid_start_y=120):
    global grid_start_x, cell_width, cell_height
    
    # Clear existing grid lines
    canvas.delete("grid_line")

    # Make grid more square - cell height determines cell width
    cell_height = (height - grid_start_y) // 6
    cell_width = cell_height
    grid_width = 7 * cell_width
    grid_start_x = (width - grid_width) // 2

    # Draw vertical lines
    for col in range(1, 7):
        x = grid_start_x + col * cell_width
        canvas.create_line(x, grid_start_y, x, height, fill="#292929", tags="grid_line")

    # Draw horizontal lines
    for row in range(1, 6):
        y = grid_start_y + row * cell_height
        canvas.create_line(grid_start_x, y, grid_start_x + grid_width, y, fill="#292929", tags="grid_line")

root = tk.Tk()

canvas = tk.Canvas(root, bg="white")
canvas.pack(fill="both", expand=True)

# Load the background image
bg_image = tk.PhotoImage(file="assets/images/paper.png")

# Add the image to the canvas
image_id = canvas.create_image(0, 0, image=bg_image, anchor="center")

# Add text to the canvas
text_id = canvas.create_text(0, 0, text="Connect 4", font=("Freestyle Script", 64), fill="#292929", anchor="n")

# Bind the resize event to the canvas
canvas.bind("<Configure>", resize_image)

# Load piece images
player1_piece = tk.PhotoImage(file="assets/images/cookie.png")
player2_piece = tk.PhotoImage(file="assets/images/button.png")

def draw_pieces():
    # Clear existing pieces
    canvas.delete("pieces")
    
    # Draw pieces based on board state
    for row in range(6):
        for col in range(7):
            if connect4_logic.board[row][col] != 0:
                x = grid_start_x + (col * cell_width) + (cell_width // 2)
                y = grid_start_y + (row * cell_height) + (cell_height // 2)
                
                if connect4_logic.board[row][col] == 1:
                    canvas.create_image(x, y, image=player1_piece, tags="pieces")
                elif connect4_logic.board[row][col] == 2:
                    canvas.create_image(x, y, image=player2_piece, tags="pieces")

# Click event to place pieces on the board
def on_canvas_click(event):
    # Calculate which column was clicked
    col = (event.x - grid_start_x) // cell_width
    
    # Validate column
    if col < 0 or col >= 7:
        return
    
    # Place the piece in the lowest available row
    for row in range(5, -1, -1):
        if connect4_logic.board[row][col] == 0:
            connect4_logic.board[row][col] = connect4_logic.turn
            
            # Switch turns
            if connect4_logic.turn == 1:
                connect4_logic.turn = 2
            else:
                connect4_logic.turn = 1
            
            # Redraw the pieces
            draw_pieces()
            break

canvas.bind("<Button-1>", on_canvas_click)

root.mainloop()

