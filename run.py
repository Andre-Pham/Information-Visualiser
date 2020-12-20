
import tkinter as tk

from display_visrep import *
from text_to_visrep import *
from visrep_to_text import *

# Constants
BACKGROUND_COLOR = "white"
TEXT_COLOR = "black"
TEXT_COLOR_HIGHLIGHT = "white"
TEXTBOX_COLOR = "#d0d0d0"
BUTTON_COLOR = "#8a69f3"
FONT = "System"

# Set up window
window = tk.Tk()
window.geometry("450x150")
window.title("VISREP")
window.configure(bg = BACKGROUND_COLOR)

# Reaction functions
def generate_visrep_button():
    text_input = text_box.get('1.0', tk.END).strip("\n")
    visrep = generate_visrep(text_input)
    generate_visrep_png(visrep)

# Declare UI features
text_box = tk.Text(
    window,
    width = 50,
    height = 3,
    font = FONT,
    relief = "flat",
    bg = TEXTBOX_COLOR,
    fg = TEXT_COLOR
)

elements = [
    tk.Label(
        window,
        text = "Enter text:",
        font = FONT,
        bg = BACKGROUND_COLOR,
        fg = TEXT_COLOR
    ),
    text_box,
    tk.Button(
        window,
        text = "Generate VISREP",
        relief = "flat",
        font = FONT,
        fg = TEXT_COLOR_HIGHLIGHT,
        bg = BUTTON_COLOR,
        command = generate_visrep_button
    )
]

# Draw UI features
for num, elmt in enumerate(elements):
    elmt.pack()
    '''
    elmt.grid(
        row = num,
        column = 0,
        sticky = "N"
    )
    '''

# Run window
window.mainloop()
