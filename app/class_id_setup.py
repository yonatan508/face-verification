import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.font import Font
from config_manager import ConfigManager  # Handles configuration settings
from centered_application import ApplicationPosition  # Helps centering the app window


class ClassIDSetupWindow:
    # Default name for the Excel file that stores attendance
    excel_file_name = "class attendance.xlsx"

    def __init__(self, master):
        self.top = tk.Toplevel(master)  # Create a new top-level window on top of the main application
        self.top.title("Setup Class ID")

        # Center the window on the screen
        app_position = ApplicationPosition(self.top)
        app_position.center_window()        

        self.config_manager = ConfigManager()  # Configuration manager instance assumed to be defined in the config_manager module

        self.setup_ui()
        self.top.attributes('-topmost', True)  # Keep window on top
        self.top.resizable(False, False)  # Disable window resizing

    def setup_ui(self):
        """Set up the user interface for the Class ID setup window."""
        # Styling and layout
        self.top.grid_columnconfigure(1, weight=1)  # Make the entry column expandable
        font = Font(family="Helvetica", size=12)

        # Class ID Entry
        ttk.Label(self.top, text="Classroom ID:", font=font).grid(column=0, row=0, padx=10, pady=10, sticky='e')
        self.id_entry = ttk.Entry(self.top, font=font)
        self.id_entry.grid(column=1, row=0, padx=10, pady=10, sticky='ew')

        # Directory Path Entry and Browse
        ttk.Label(self.top, text="Directory Path:", font=font).grid(column=0, row=1, padx=10, pady=10, sticky='e')
        self.directory_entry = ttk.Entry(self.top, font=font)
        self.directory_entry.grid(column=1, row=1, padx=10, pady=10, sticky='ew')
        self.directory_btn = ttk.Button(self.top, text="Browse", command=self.browse_directory)
        self.directory_btn.grid(column=2, row=1, padx=10, pady=10)

        # Excel File Path Entry and Browse
        ttk.Label(self.top, text="Excel File Save Location:", font=font).grid(column=0, row=2, padx=10, pady=10, sticky='e')
        self.file_path_entry = ttk.Entry(self.top, font=font)
        self.file_path_entry.grid(column=1, row=2, padx=10, pady=10, sticky='ew')
        self.browse_file_button = ttk.Button(self.top, text="Browse", command=self.browse_file)
        self.browse_file_button.grid(column=2, row=2, padx=10, pady=10)

        # Finalize Button
        self.finalize_button = ttk.Button(self.top, text="Finalize", command=self.submit)
        self.finalize_button.grid(column=0, row=3, columnspan=3, pady=10, sticky='nsew')  # Center the button by spanning across all columns

    def browse_directory(self):
        """Handle the directory browsing and set the directory path."""
        self.top.attributes('-topmost', False)  # Temporarily remove topmost attribute

        self.directory = filedialog.askdirectory()

        self.top.attributes('-topmost', True)  # Restore topmost attribute

        if self.directory:
            self.directory_entry.delete(0, tk.END)
            self.directory_entry.insert(0, self.directory)
            self.directory_entry.config(state="readonly")

    def browse_file(self):
        """Handle the file path browsing for saving the Excel file."""
        self.top.attributes('-topmost', False)  # Temporarily remove topmost attribute

        file_directory = filedialog.askdirectory()

        self.top.attributes('-topmost', True)  # Restore topmost attribute
        
        if file_directory:
            self.excel_file_path = os.path.join(file_directory, self.excel_file_name)
            self.file_path_entry.delete(0, tk.END)
            self.file_path_entry.insert(0, self.excel_file_path)
            self.file_path_entry.config(state="readonly")

    def submit(self):
        """Validate inputs and save configuration, then close the window if successful."""
        class_id = self.id_entry.get().strip()

        if class_id and hasattr(self, 'directory') and hasattr(self, 'excel_file_path'):
            self.config_manager.set_class_config(class_id=class_id, directory_path=self.directory, excel_file_path=self.excel_file_path)
            messagebox.showinfo("Success", "Class ID and directory path have been set successfully.")
            self.top.destroy()
        else:
            messagebox.showerror("Error", "Please ensure all fields are filled out correctly.")
