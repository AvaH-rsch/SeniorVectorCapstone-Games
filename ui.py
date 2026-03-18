from tkinter import *
import tkinter as tk
from tkinter import font

def resize_image(event):
    # Resize the canvas to match the window size
    canvas.config(width=event.width, height=event.height)
    # Redraw the image at the center of the canvas
    canvas.coords(image_id, event.width // 2, event.height // 2)
    # Keep the text at the top center
    canvas.coords(text_id, event.width // 2, 20)

    # Redraw the grid to fit the resized canvas
    draw_grid(event.width, event.height)

def draw_grid(width, height):
    # Clear existing grid lines
    canvas.delete("grid_line")

    # Calculate cell size based on canvas dimensions
    cell_width = width // 7
    cell_height = height // 6 

    # Draw vertical lines
    for col in range(1, 7):
        x = col * cell_width
        canvas.create_line(x, 0, x, height, fill="#292929", tags="grid_line")

    # Draw horizontal lines
    for row in range(1, 6):
        y = row * cell_height
        canvas.create_line(0, y, width, y, fill="#292929", tags="grid_line")

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



root.mainloop()

