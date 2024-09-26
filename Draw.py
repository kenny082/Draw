"""
Drawing App inspired by Microsoft Paint

@author Kenny
"""

import tkinter as tk
from tkinter import colorchooser, simpledialog
import random

# Create the main window
root = tk.Tk()
root.title("Drawing App")

current_color = "#000000"  # Default is black (hex format)
eraser_mode = False  # Track whether eraser is active
pen_type = "default"  # Track pen type
pen_size = 5  # Default pen size

# Track the position of dragged items
selected_item = None
dragged_item_x = 0
dragged_item_y = 0
drawing_enabled = True  # Track if drawing is enabled

# Create a canvas where users can draw
canvas = tk.Canvas(root, width = 800, height = 600, bg = "white")
canvas.pack(fill = "both", expand = True)

# Function to paint or erase on the canvas
def paint(event):
    if not drawing_enabled:  # Disable painting if dragging text
        return
    global pen_size

    # Check if the eraser is active
    if eraser_mode:
        x1, y1 = (event.x - pen_size), (event.y - pen_size)
        x2, y2 = (event.x + pen_size), (event.y + pen_size)
        canvas.create_oval(x1, y1, x2, y2, fill = "white", outline = "white", width = pen_size)
    else:
        if pen_type == "default":
            x1, y1 = (event.x - pen_size), (event.y - pen_size)
            x2, y2 = (event.x + pen_size), (event.y + pen_size)
            canvas.create_oval(x1, y1, x2, y2, fill = current_color, outline = current_color, width = pen_size)
        elif pen_type == "rainbow":
            rainbow_color = f"#{random.randint(0, 0xFFFFFF):06x}"
            x1, y1 = (event.x - pen_size), (event.y - pen_size)
            x2, y2 = (event.x + pen_size), (event.y + pen_size)
            canvas.create_oval(x1, y1, x2, y2, fill = rainbow_color, outline = rainbow_color, width = pen_size)

# Function to change the current drawing color
def change_color(new_color):
    global current_color
    current_color = new_color
    hex_input.delete(0, tk.END)
    hex_input.insert(0, current_color)

# Function to open the color picker (RGB Color Wheel)
def choose_color():
    global current_color
    color = colorchooser.askcolor(title = "Choose a color")
    if color[1]:  # Check if a color is selected
        change_color(color[1])  # Update to the selected color (hex value)

# Function to change color via hex input
def change_color_from_hex():
    hex_code = hex_input.get()
    if len(hex_code) == 7 and hex_code[0] == "#":  # Validate hex code format
        change_color(hex_code)

# Function to toggle the eraser mode
def toggle_eraser():
    global eraser_mode
    eraser_mode = not eraser_mode
    if eraser_mode:
        eraser_button.config(relief = tk.SUNKEN)  # Sinks the button to show it is active
    else:
        eraser_button.config(relief = tk.RAISED)  # Raises the button show it is no longer active

# Function to set pen type to default
def set_normal_pen():
    global pen_type, eraser_mode
    pen_type = "default"
    if eraser_mode:
        eraser_mode = False
        eraser_button.config(relief = tk.RAISED)

# Function to set pen type to rainbow
def set_rainbow_pen():
    global pen_type, eraser_mode
    pen_type = "rainbow"
    if eraser_mode:
        eraser_mode = False
        eraser_button.config(relief = tk.RAISED)

def change_pen_size(new_size):
    global pen_size
    pen_size = int(new_size)

# Function to clear the canvas
def clear_board():
    canvas.delete("all")

# Function to add text to the canvas
def add_text():
    text = simpledialog.askstring("Input", "Enter text:")
    if text:  # Check if input is not empty
        # Calculate center position
        x = canvas.winfo_width() // 2
        y = canvas.winfo_height() // 2
        text_id = canvas.create_text(x, y, text = text, fill = current_color, font = ("Arial", 12))

        # Bind the double-click event to edit text
        canvas.tag_bind(text_id, "<Double-1>", lambda e, t=text_id: edit_text(t))
        # Bind the click-and-drag event for dragging the text
        canvas.tag_bind(text_id, "<ButtonPress-1>", on_item_click)
        canvas.tag_bind(text_id, "<B1-Motion>", drag_item)

# Function to edit text on double-click
def edit_text(text_id):
    current_text = canvas.itemcget(text_id, "text")
    new_text = simpledialog.askstring("Edit Text", "Enter new text:", initialvalue = current_text)
    if new_text is not None:  # Check if input is not canceled
        canvas.itemconfig(text_id, text = new_text)

# Function to handle click event on items
def on_item_click(event):
    global selected_item, dragged_item_x, dragged_item_y, drawing_enabled
    selected_item = canvas.find_closest(event.x, event.y)[0]
    dragged_item_x = event.x
    dragged_item_y = event.y
    drawing_enabled = False  # Disable drawing while dragging

# Function to drag items
def drag_item(event):
    global selected_item, dragged_item_x, dragged_item_y
    if selected_item:
        dx = event.x - dragged_item_x
        dy = event.y - dragged_item_y
        canvas.move(selected_item, dx, dy)
        dragged_item_x = event.x
        dragged_item_y = event.y

# Function to release dragging
def on_release(event):
    global drawing_enabled
    drawing_enabled = True  # Re-enable drawing after dragging

# Bind the release event to re-enable drawing
canvas.bind("<ButtonRelease-1>", on_release)

# Bind the paint function to left mouse button motion (drag to draw)
canvas.bind("<B1-Motion>", paint)

# Create a frame to hold the color buttons and hex input
color_frame = tk.Frame(root)
color_frame.pack()

# Button to open RGB color wheel (color chooser)
color_picker_button = tk.Button(color_frame, text = "Colors", command = choose_color)
color_picker_button.pack(side = "left", padx = 5)

# Input field for hex code
hex_label = tk.Label(color_frame, text = "Hex Code:")
hex_label.pack(side = "left")
hex_input = tk.Entry(color_frame, width = 10)
hex_input.pack(side = "left", padx = 5)
hex_input.insert(0, current_color)

# Button to apply hex color
apply_hex_button = tk.Button(color_frame, text = "Apply", command = change_color_from_hex)
apply_hex_button.pack(side = "left", padx = 5)

# Button to toggle eraser mode
eraser_button = tk.Button(color_frame, text = "Eraser", command = toggle_eraser)
eraser_button.pack(side = "left", padx = 5)

# Button to set default pen type
normal_pen_button = tk.Button(color_frame, text = "Default Pen", command = set_normal_pen)
normal_pen_button.pack(side = "left", padx = 5)

# Button to set rainbow pen type
rainbow_pen_button = tk.Button(color_frame, text="Rainbow Pen", command=set_rainbow_pen)
rainbow_pen_button.pack(side = "left", padx = 5)

# Create a slider for pen size
size_slider = tk.Scale(color_frame, from_ = 1, to = 10, orient = tk.HORIZONTAL,
                       label = "Pen Size", command = change_pen_size)
size_slider.set(pen_size)
size_slider.pack(side = "left", padx = 5)

# Button to clear the board
clear_button = tk.Button(color_frame, text = "Clear Board", command = clear_board)
clear_button.pack(side = "left", padx = 5)

# Button to add text
text_button = tk.Button(color_frame, text = "Add Text", command = add_text)
text_button.pack(side = "left", padx = 5)

# Start the Tkinter main loop
root.mainloop()