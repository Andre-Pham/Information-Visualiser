
import tkinter as tk

from display_visrep import *
from text_to_visrep import *
from visrep_to_text import *

# Constants
BACKGROUND_COLOR = "white"
TEXT_COLOR = "black"
TEXT_BACK_COLOR = "#d0d0d0"

# Set up window
window = tk.Tk()
window.geometry("600x300")
window.title("VISREP")
window.configure(bg = BACKGROUND_COLOR)

# Reaction functions
def generate_visrep_button():
    text_input = text_box.get('1.0', tk.END)
    visrep = generate_visrep(text_input)
    generate_visrep_png(visrep)

# Declare UI features
text_box = tk.Text(
    window,
    width = 50,
    height = 3,
    font = "none 12 bold",
    bg = TEXT_BACK_COLOR,
    fg = TEXT_COLOR
)

elements = [
    tk.Label(
        window,
        text = "Enter text:",
        font = "none 15 bold",
        bg = BACKGROUND_COLOR,
        fg = TEXT_COLOR
    ),
    text_box,
    tk.Button(
        window,
        text = "Generate VISREP",
        font = "none 12 bold",
        command = generate_visrep_button
    )
]

# Draw UI features
for num, elmt in enumerate(elements):
    elmt.grid(
        row = num,
        column = 0,
        sticky = "W"
    )

# Run window
window.mainloop()
