import os
import pandas as pd
import tkinter as tk
from tkinter.font import Font
from tkinter import filedialog, messagebox, ttk
from config_manager import ConfigManager
from face_recognition_manager import FaceRecognitionManager
from centered_application import ApplicationPosition

class RecognitionWindow:
    def __init__(self, master, callback=None):
        self.master = master
        self.callback = callback  # Optional function to run after processing

        # Create a top-level window for face recognition settings
        self.top = tk.Toplevel(self.master)
        self.top.title("Face Recognition")

        # Center the window on the screen
        app_position = ApplicationPosition(self.top)
        app_position.center_window()

        # Initialize configuration manager
        self.config_manager = ConfigManager()

        # Set up the UI elements
        self.setup_ui()
        self.top.attributes('-topmost', True)  # Make window always stay on top
        self.top.resizable(False,False)  # Prevent the window from being resized

    def setup_ui(self):
        # Configure the font and layout for the UI
        font = Font(family="Helvetica", size=12)

        # Configure grid layout for evenly spacing the elements
        self.top.grid_columnconfigure(0, weight=1)
        self.top.grid_columnconfigure(1, weight=1)
        self.top.grid_columnconfigure(2, weight=1)

        # Label and dropdown menu for class selection
        ttk.Label(self.top, text="Select Classroom ID:", font=font).grid(row=1, column=0, padx=(20, 0), sticky='e')
        self.class_var = tk.StringVar(value="Select your desired classroom")
        classes_id = list(self.config_manager.load_config().keys())
        self.dropDownMenu = ttk.OptionMenu(self.top, self.class_var, self.class_var.get(), *classes_id)
        self.dropDownMenu.grid(row=1, column=1, sticky='w', padx=(20, 20), pady=(20, 20))

        # Entry field and button for selecting an anchor image path
        ttk.Label(self.top, text="Anchor Image Path:", font=font).grid(row=2, column=0, pady=(0, 20), sticky='e')
        self.anchor_image_path_entry = ttk.Entry(self.top, font=font)
        self.anchor_image_path_entry.grid(row=2, column=1, pady=(0, 20), padx=20, sticky='ew')
        self.anchor_image_path_btn = ttk.Button(self.top, text="Browse", command=self.browse_anchor)
        self.anchor_image_path_btn.grid(row=2, column=2, pady=(0, 20), padx=(0, 20), sticky='w')

        # Button to initiate the process
        self.process_button = ttk.Button(self.top, text="Process", command=self.process, state="disabled")
        self.process_button.grid(row=3, column=0, columnspan=3, pady=20, sticky='ew')

        # Make the middle column expand more to accommodate the entry widget
        self.top.grid_columnconfigure(1, weight=3)

    def browse_anchor(self):
        # Open a file dialog to choose an image file, and update UI accordingly
        self.top.attributes('-topmost', False)  # Temporarily make window not stay on top
        self.anchor_image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        self.top.attributes('-topmost', True)  # Restore window topmost status

        # Update the entry field and enable the process button if a file is selected
        if self.anchor_image_path:
            self.anchor_image_path_entry.delete(0, tk.END)
            self.anchor_image_path_entry.insert(0, self.anchor_image_path)
            self.anchor_image_path_btn.config(state="readonly")
            self.process_button.config(state="normal")

    def load_attributes(self):
        # Load configuration specific to the selected class ID
        try:
            class_config = self.config_manager.get_class_config(str(self.class_id))
            self.directory_path, self.file_path = class_config.values()
        except ValueError:
            messagebox.showerror("Configuration Error", "Invalid configuration for the selected class.")
            return False
        else:
            return True

    def load_file(self):
        # Load or initialize the DataFrame depending on the file's existence
        if os.path.isfile(self.file_path):
            self.df = pd.read_excel(self.file_path, index_col=0)
            # Uniform formatting for column names
            self.df.columns = pd.to_datetime(self.df.columns).strftime("%Y-%m-%d")
        else:
            # Initialize a new DataFrame if file doesn't exist
            self.initialize_dataframe_from_directory()

    def initialize_dataframe_from_directory(self):
        # Create a DataFrame using image filenames as index
        file_names = [
            filename.replace("_", " ")[:filename.rindex(".")].strip().capitalize()
            for filename in sorted(os.listdir(self.directory_path), key=lambda label: ord(label[0]))
            if filename.lower().endswith(('.png', '.jpg', '.jpeg'))
        ]

        if not file_names:
            messagebox.showerror("FileExistsError", "No image files found in the directory.")
            self.config_manager.delete_class_config(self.class_id)
            

        self.df = pd.DataFrame(index=file_names)

    def process(self):
        # Main processing function
        self.top.attributes("-topmost", False)
        self.master.attributes("-topmost", False)

        self.class_id = str(self.class_var.get())
        print(self.class_id)

        if not self.load_attributes():
            return

        try:
            self.load_file()
        except PermissionError:
            messagebox.showerror("PermissionError", "Attendance updated Failed.\n please close the excel file and try again")
            return

        if not all([hasattr(self, 'directory_path'), hasattr(self, 'anchor_image_path'), hasattr(self, 'file_path')]):
            messagebox.showerror("Error", "Please ensure all paths are set.")
            return

        # Face recognition processing and results handling
        self.face_manager = FaceRecognitionManager(self.directory_path, self.anchor_image_path, self.file_path)
        cropped_faces = self.face_manager.crop_faces()
        results = self.face_manager.compare_faces(cropped_faces)
        self.face_manager.update_dataframe(results, self.df)
        
        messagebox.showinfo("Success", "Attendance updated successfully.")

        # Optionally close the window and run the callback
        self.master.destroy()
        try:
            if self.callback:
                self.callback(self.file_path)
        except PermissionError:
            messagebox.showerror("PermissionError", "Attendance updated Failed.\n please close the excel file and try again")
            return
