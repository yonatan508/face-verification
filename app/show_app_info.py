import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
from centered_application import ApplicationPosition

class ApplicationInstructionManual:
    # Static variable for the file that contains the app instructions
    filename = "app description.txt"

    def __init__(self, master):
        self.master = master
        self.top = tk.Toplevel(master)  # Create a top-level window
        self.top.resizable(False, False)
        self.top.title("About the App")

        # Center the window using ApplicationPosition
        info_position = ApplicationPosition(self.top)
        info_position.center_window()

        # Set up the user interface
        self.setup_ui()

        # Keep this window on top
        self.top.attributes("-topmost", True)
    
    @property
    def app_instructions(self):
        """Property to load and return the app instructions from the set filename."""
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError:
            return "Description file not found."

    def setup_ui(self):
        """Create the UI components for the instruction manual."""
        # Configure the font for the text widget
        app_font = Font(family="Arial", size=12)

        # Create a scrollable frame for the instructions
        description_frame = ttk.Frame(self.top, padding=(10, 10))
        description_frame.pack(fill=tk.BOTH, expand=True)

        # Create the Text widget
        description_text = tk.Text(
            description_frame, 
            wrap=tk.WORD, 
            font=app_font, 
            padx=10, 
            pady=10,
            yscrollcommand=lambda *args: scrollbar.set(*args)
        )
        
        # Add the app instructions with right alignment
        description_text.insert(tk.END, self.app_instructions)
        description_text.tag_add("right_align", "1.0", tk.END)
        description_text.tag_configure("right_align", justify="right")
        description_text.config(state=tk.DISABLED)

        # Create a scrollbar for the text widget
        scrollbar = ttk.Scrollbar(description_frame, orient=tk.VERTICAL, command=description_text.yview)

        description_text.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        description_frame.rowconfigure(0, weight=1)
        description_frame.columnconfigure(0, weight=1)
