# Code for running the interface and connecting the entire program together

# Import modules
import tkinter as tk
from tkinter import filedialog
import sys
# Import complimenting scripts
from gen_visrep_photo import *
from gen_visrep_matrix import *
from read_visrep_matrix import *
from read_visrep_photo_dev import *
from constants_dev import *

def common_title(text):
    '''
    A label object with all consistent aesthetic features for titles used in the
    interface.
    '''
    return tk.Label(
        window,
        text=text,
        font=FONT,
        bg=BACKGROUND_COLOR,
        fg=TEXT_COLOR
    )

def common_button(text, command):
    '''
    A button object with all consistent aesthetic features for buttons used in
    the interface.
    '''
    return tk.Button(
        window,
        text=text,
        relief="flat",
        font=FONT,
        fg=TEXT_COLOR_HIGHLIGHT,
        bg=BUTTON_COLOR,
        width=BUTTON_WIDTH,
        command=command
    )

def common_text_input():
    '''
    A textbox object for text input with all consistent aesthetic features for
    texboxes used in the interface.
    '''
    return tk.Text(
        window,
        width=50,
        height=3,
        font=FONT,
        relief="flat",
        bg=TEXTBOX_COLOR,
        fg=TEXT_COLOR
    )

def common_text_output():
    '''
    A textbox object for text output with all consistent aesthetic features for
    textboxes used in the interface.
    '''
    return tk.Label(
        window,
        width=50,
        height=3,
        font=FONT,
        bg=TEXTBOX_COLOR,
        fg=TEXT_COLOR
    )

def common_popup(title, message):
    '''
    A popup object with all consistent aesthetic features for popup boxes used
    in the interface.
    '''
    popup=tk.Toplevel()
    popup.geometry("350x100")
    popup.title(title)
    popup.iconbitmap(DIR_LOGO)
    tk.Label(
        popup,
        text=message,
        font=FONT,
        height=3
    ).pack()
    tk.Button(
        popup,
        text="Close",
        relief="flat",
        font=FONT,
        fg=TEXT_COLOR_HIGHLIGHT,
        bg=BUTTON_COLOR,
        width=BUTTON_WIDTH,
        command=popup.destroy
    ).pack()
    popup.mainloop()

class Interface:
    def __init__(self, window, geometry, title, bg):
        # Define interface object for the application
        self.window = window
        # Define list which tracks of all tkinter objects being displayed
        # on the interface (so that they can be removed when necessary)
        self.drawn_elements = []
        # Define current textbox object in use, so that it can easily be updated
        self.live_text_box = None

        # Set properties of interface
        window.geometry(geometry)
        window.title(title)
        window.configure(bg=bg)
        window.iconbitmap(DIR_LOGO)

        # Set grid configurations of interface
        window.grid_rowconfigure(0, weight=0)
        window.grid_columnconfigure(0, weight=1)

        # Define tkinter elements for the main menu page
        self.main_menu_elements = [
            common_title("Main Menu [DEVELOPER MODE]"),
            common_button("Text to VISREP", lambda: self.draw_gen_visrep()),
            common_button("VISREP to Text", lambda: self.draw_gen_text()),
            common_button("Quit", lambda: self.quit_interface())
        ]

        # Define tkinter elements for the 'text to visrep' page
        self.gen_visrep_elements = [
            common_title("Text to VISREP [DEVELOPER MODE]"),
            common_text_input(),
            common_button("Generate VISREP", lambda: self.generate_visrep_button()),
            common_button("Save VISREP", lambda: self.save_visrep_button()),
            common_button("Main Menu", lambda: self.draw_main_menu())
        ]

        # Define tkinter elements for the 'visrep to text' page
        self.gen_text_elements = [
            common_title("VISREP to Text [DEVELOPER MODE]"),
            common_button("Select Image", lambda: self.translate_visrep_button()),
            common_text_output(),
            common_button("Main Menu", lambda: self.draw_main_menu())
        ]

    # FUNCTIONS TO UPDATE AND CHANGE INTERFACE

    def quit_interface(self):
        '''
        Closes the application.
        '''
        window.destroy()
        popup.destroy()
        exit()

    def clear_all(self):
        '''
        Removes all elements from the interface.
        '''
        for elmt in self.drawn_elements:
            elmt.grid_forget()

    def change_elements(self, element_list):
        '''
        Re-draws all elements on the interface with others from a given list.
        '''
        self.clear_all()
        self.drawn_elements = []

        for order, elmt in enumerate(element_list):
            elmt.grid(
                pady=5,
                row=order,
                column=0
            )
            self.drawn_elements.append(elmt)

    def draw_main_menu(self):
        '''
        Changes all elements on the interface to display main menu page.
        '''
        self.change_elements(self.main_menu_elements)

    def draw_gen_visrep(self):
        '''
        Changes all elements on the interface to display 'text to visrep' page.
        '''
        self.change_elements(self.gen_visrep_elements)
        self.live_text_box = self.gen_visrep_elements[1]
        self.live_text_box.delete('1.0', tk.END)

    def draw_gen_text(self):
        '''
        Changes all elements on the interface to display 'visrep to text' page.
        '''
        self.change_elements(self.gen_text_elements)
        self.live_text_box = self.gen_text_elements[2]
        self.live_text_box.config(
            text="",
            bg=TEXTBOX_COLOR,
            fg=TEXT_COLOR
        )

    # FUNCTIONS THAT REACT TO USER INTERACTION

    def generate_visrep_button(self):
        '''
        Generates a png visrep, and displays it to the user. Activates from
        "Generate VISREP" button.
        '''
        try:
            text_input = self.live_text_box.get('1.0', tk.END).strip("\n")
            visrep = gen_visrep_matrix(text_input)
            gen_visrep_photo(visrep, "show")
        except:
            common_popup(
                "An Error Occured",
                "The VISREP could not be generated."
            )

    def save_visrep_button(self):
        '''
        Generates a png visrep, and saves it to a directory. Activates from
        "Save VISREP" button.
        '''
        try:
            text_input = self.live_text_box.get('1.0', tk.END).strip("\n")
            visrep = gen_visrep_matrix(text_input)
            gen_visrep_photo(visrep, self.select_save_dir(text_input))
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
        '''
        Generates text from a visrep image file, selected via file explorer.
        Activates from "Select Image" button.
        '''
        #try:
        visrep_dir = self.select_image()
        visrep_matrix = read_visrep_photo(visrep_dir)
        text_output = read_visrep_matrix(visrep_matrix)
        self.live_text_box.config(
            text=text_output,
            bg=SUCCESS_COLOR,
            fg=TEXT_COLOR_HIGHLIGHT
        )
        '''
        except:
            self.live_text_box.config(
                text="ERROR: Scan unsuccessful.",
                bg=FAIL_COLOR,
                fg=TEXT_COLOR_HIGHLIGHT
            )
        '''

    # FUNCTIONS THAT SUPPORT FILE SELECTION

    def select_image(self):
        '''
        Allows the user to select a file in any given directory.
        '''
        return filedialog.askopenfilename(
            initialdir="/",
            title="Select jpeg/png",
            filetypes=(
                ("jpeg/png","*.png *.jpg"),
                ("all files","*.*")
            )
        )

    def select_save_dir(self, save_name):
        '''
        Allows the user to select a directory to save a visrep png to.
        '''
        if sys.platform.startswith("win32"):
            # Windows
            banned_char = "<>:\"/\|?*"
        elif sys.platform.startswith("linux"):
            # Linux
            banned_char = "/"
        elif sys.platform.startswith("darwin"):
            # MacOS
            banned_char = ":"
        else:
            banned_char = []
        for char in banned_char:
            save_name = save_name.replace(char, "#")
        return filedialog.asksaveasfilename(
            initialdir="/",
            title="Select directory",
            initialfile=f"VISREP[{save_name}]",
            defaultextension=".png",
            filetypes=(
                ("png","*.png"),
                ("all files","*.*")
            )
        )

# Set up window
window = tk.Tk()
interface = Interface(window, "450x215", "VISREP", BACKGROUND_COLOR)
interface.draw_main_menu()

# Run window
window.mainloop()
