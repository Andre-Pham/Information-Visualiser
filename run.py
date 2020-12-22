
import tkinter as tk
from tkinter import filedialog

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
        self.live_directory = ""

        window.geometry(geometry)
        window.title(title)
        window.configure(bg = bg)

        window.grid_rowconfigure(0, weight=0)
        window.grid_columnconfigure(0, weight=1)

        self.main_menu_elements = [
            tk.Label(
                window,
                text = "Main Menu",
                font = FONT,
                bg = BACKGROUND_COLOR,
                fg = TEXT_COLOR
            ),
            tk.Button(
                window,
                text = "Text to VISREP",
                relief = "flat",
                font = FONT,
                fg = TEXT_COLOR_HIGHLIGHT,
                bg = BUTTON_COLOR,
                command = lambda: self.draw_gen_visrep()
            ),
            tk.Button(
                window,
                text = "VISREP to Text",
                relief = "flat",
                font = FONT,
                fg = TEXT_COLOR_HIGHLIGHT,
                bg = BUTTON_COLOR,
                command = lambda: self.draw_gen_text()
            ),
        ]

        self.gen_visrep_elements = [
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

        self.gen_text_elements = [
            tk.Label(
                window,
                text = "Select Image",
                font = FONT,
                bg = BACKGROUND_COLOR,
                fg = TEXT_COLOR
            ),
            tk.Button(
                window,
                text = "Select Image",
                relief = "flat",
                font = FONT,
                fg = TEXT_COLOR_HIGHLIGHT,
                bg = BUTTON_COLOR,
                command = lambda: self.select_image()
            )
        ]

    def clear_all(self):
        for elmt in self.drawn_elements:
            elmt.pack_forget()

    def draw_main_menu(self):
        self.clear_all()
        self.drawn_elements = []

        for order, elmt in enumerate(self.main_menu_elements):
            elmt.grid(
                pady = 5,
                row = order,
                column = 0
            )
            self.drawn_elements.append(elmt)

    def draw_gen_visrep(self):
        self.clear_all()
        self.drawn_elements = []

        self.live_text_box = self.gen_visrep_elements[1]

        for elmt in self.gen_visrep_elements:
            elmt.pack()
            self.drawn_elements.append(elmt)

    def draw_gen_text(self):
        self.clear_all()
        self.drawn_elements = []

        for elmt in self.gen_text_elements:
            elmt.pack()
            self.drawn_elements.append(elmt)

    # Reaction functions
    def generate_visrep_button(self):
        text_input = self.live_text_box.get('1.0', tk.END).strip("\n")
        visrep = generate_visrep(text_input)
        generate_visrep_png(visrep)

    def select_image(self):
        return filedialog.askopenfilename(
            initialdir = "/",
            title = "Select file",
            filetypes = (
                ("jpeg or png files","*.png *.jpg"),
                ("all files","*.*")
            )
        )

    def select_save_dir(self):
        return filedialog.asksaveasfilename(
            initialdir = "/",
            title = "Select file",
            filetypes = (
                ("png","*.png"),
                ("jpeg","*.jpg"),
                ("all files","*.*")
            )
        )

# Set up window
window = tk.Tk()
interface = Interface(window, "450x150", "VISREP", BACKGROUND_COLOR)
interface.draw_main_menu()

# Run window
window.mainloop()
