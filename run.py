
# Import modules
import tkinter as tk
from tkinter import filedialog
# Import complimenting scripts
from display_visrep import *
from text_to_visrep import *
from visrep_to_text import *
from scan_visrep import *
from constants import *

def common_title(text):
    return tk.Label(
        window,
        text = text,
        font = FONT,
        bg = BACKGROUND_COLOR,
        fg = TEXT_COLOR
    )

def common_button(text, command):
    return tk.Button(
        window,
        text = text,
        relief = "flat",
        font = FONT,
        fg = TEXT_COLOR_HIGHLIGHT,
        bg = BUTTON_COLOR,
        width = BUTTON_WIDTH,
        command = command
    )

def common_text():
    return tk.Text(
        window,
        width = 50,
        height = 3,
        font = FONT,
        relief = "flat",
        bg = TEXTBOX_COLOR,
        fg = TEXT_COLOR
    )

def common_popup(title, message):
    popup = tk.Toplevel()
    popup.geometry("350x100")
    popup.title(title)
    popup.iconbitmap("logo.ico")
    tk.Label(
        popup,
        text = message,
        font = FONT,
        height = 3
    ).pack()
    tk.Button(
        popup,
        text = "Close",
        relief = "flat",
        font = FONT,
        fg = TEXT_COLOR_HIGHLIGHT,
        bg = BUTTON_COLOR,
        width = BUTTON_WIDTH,
        command = popup.destroy
    ).pack()
    popup.mainloop()

class Interface:
    def __init__(self, window, geometry, title, bg):
        self.window = window
        self.drawn_elements = []
        self.live_text_box = None
        self.live_directory = ""

        window.geometry(geometry)
        window.title(title)
        window.configure(bg = bg)
        window.iconbitmap("logo.ico")

        window.grid_rowconfigure(0, weight = 0)
        window.grid_columnconfigure(0, weight = 1)

        self.main_menu_elements = [
            common_title("Main Menu"),
            common_button("Text to VISREP", lambda: self.draw_gen_visrep()),
            common_button("VISREP to Text", lambda: self.draw_gen_text()),
            common_button("Quit", lambda: self.quit_interface())
        ]

        self.gen_visrep_elements = [
            common_title("Text to VISREP"),
            common_text(),
            common_button("Generate VISREP", lambda: self.generate_visrep_button()),
            common_button("Save VISREP", lambda: self.save_visrep_button()),
            common_button("Main Menu", lambda: self.draw_main_menu())
        ]

        self.gen_text_elements = [
            common_title("VISREP to Text"),
            common_button("Select Image", lambda: self.translate_visrep_button()),
            tk.Label(
                window,
                width = 50,
                height = 3,
                font = FONT,
                bg = TEXTBOX_COLOR,
                fg = TEXT_COLOR
            ),
            common_button("Main Menu", lambda: self.draw_main_menu())
        ]

    def quit_interface(self):
        window.destroy()
        popup.destroy()
        exit()

    def clear_all(self):
        for elmt in self.drawn_elements:
            elmt.grid_forget()

    def change_elements(self, element_list):
        self.clear_all()
        self.drawn_elements = []

        for order, elmt in enumerate(element_list):
            elmt.grid(
                pady = 5,
                row = order,
                column = 0
            )
            self.drawn_elements.append(elmt)

    def draw_main_menu(self):
        self.change_elements(self.main_menu_elements)

    def draw_gen_visrep(self):
        self.change_elements(self.gen_visrep_elements)
        self.live_text_box = self.gen_visrep_elements[1]
        self.live_text_box.delete('1.0', tk.END)

    def draw_gen_text(self):
        self.change_elements(self.gen_text_elements)
        self.live_text_box = self.gen_text_elements[2]
        self.live_text_box.config(
            text = "",
            bg = TEXTBOX_COLOR,
            fg = TEXT_COLOR
        )

    # Reaction functions
    def generate_visrep_button(self):
        try:
            text_input = self.live_text_box.get('1.0', tk.END).strip("\n")
            visrep = generate_visrep(text_input)
            generate_visrep_png(visrep, "show")
        except:
            common_popup(
                "An Error Occured",
                "The VISREP could not be generated."
            )

    def save_visrep_button(self):
        try:
            text_input = self.live_text_box.get('1.0', tk.END).strip("\n")
            visrep = generate_visrep(text_input)
            generate_visrep_png(visrep, self.select_save_dir(text_input))
            common_popup(
                "File Save Successful",
                "The file was saved successfully."
            )
        except:
            common_popup(
                "Something Happened",
                "The VISREP could either not be generated or saved."
            )

    def translate_visrep_button(self):
        try:
            visrep_image = self.select_image()
            visrep_matrix = scan_visrep(visrep_image)
            text_output = decode_visrep(visrep_matrix)
            self.live_text_box.config(
                text = text_output,
                bg = SUCCESS_COLOR,
                fg = TEXT_COLOR_HIGHLIGHT
            )
        except:
            self.live_text_box.config(
                text = "ERROR: Scan unsuccessful.",
                bg = FAIL_COLOR,
                fg = TEXT_COLOR_HIGHLIGHT
            )

    def select_image(self):
        return filedialog.askopenfilename(
            initialdir = "/",
            title = "Select file",
            filetypes = (
                ("jpeg/png","*.png *.jpg"),
                ("all files","*.*")
            )
        )

    def select_save_dir(self, save_name):
        return filedialog.asksaveasfilename(
            initialdir = "/",
            title = "Select image file",
            initialfile = f"VISREP[{save_name}]",
            defaultextension = ".png",
            filetypes = (
                ("png","*.png"),
                ("jpeg","*.jpg"),
                ("all files","*.*")
            )
        )

# Set up window
window = tk.Tk()
interface = Interface(window, "450x215", "VISREP", BACKGROUND_COLOR)
interface.draw_main_menu()

# Run window
window.mainloop()
