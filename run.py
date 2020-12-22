
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

class Interface:
    def __init__(self, window, geometry, title, bg):
        self.window = window
        self.drawn_elements = []
        self.live_text_box = None

        window.geometry(geometry)
        window.title(title)
        window.configure(bg = bg)

        self.text_to_visrep_interface = [
            tk.Label(
                window,
                text = "Enter text:",
                font = FONT,
                bg = BACKGROUND_COLOR,
                fg = TEXT_COLOR
            ),
            tk.Text(
                window,
                width = 50,
                height = 3,
                font = FONT,
                relief = "flat",
                bg = TEXTBOX_COLOR,
                fg = TEXT_COLOR
            ),
            tk.Button(
                window,
                text = "Generate VISREP",
                relief = "flat",
                font = FONT,
                fg = TEXT_COLOR_HIGHLIGHT,
                bg = BUTTON_COLOR,
                command = lambda: self.generate_visrep_button()
            )
        ]

    def clear_all(self):
        for elmt in self.drawn_elements:
            elmt.pack_forget()

    def draw_text_to_visrep(self):
        self.clear_all()
        self.drawn_elements = []

        self.live_text_box = self.text_to_visrep_interface[1]

        for elmt in self.text_to_visrep_interface:
            elmt.pack()
            self.drawn_elements.append(elmt)

    # Reaction functions
    def generate_visrep_button(self):
        text_input = self.live_text_box.get('1.0', tk.END).strip("\n")
        visrep = generate_visrep(text_input)
        generate_visrep_png(visrep)


# Set up window
window = tk.Tk()
interface = Interface(window, "450x150", "VISREP", BACKGROUND_COLOR)
interface.draw_text_to_visrep()

# Run window
window.mainloop()
