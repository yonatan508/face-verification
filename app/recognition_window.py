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
        self.callback = callback

        self.top = tk.Toplevel(self.master)
        self.top.title("Face Recognition")

        app_position = ApplicationPosition(self.top)
        app_position.center_window() 

        self.config_manager = ConfigManager()  # Assume this is defined elsewhere

        self.setup_ui()
        self.top.attributes('-topmost', True)  # Keep window on top
        self.top.resizable(False,False)

    def setup_ui(self):
        font = Font(family="Helvetica", size=12)

        # Grid column configuration for layout management
        self.top.grid_columnconfigure(0, weight=1)
        self.top.grid_columnconfigure(1, weight=1)
        self.top.grid_columnconfigure(2, weight=1)

        # Label and Dropdown for class selection
        ttk.Label(self.top, text="Select Classroom ID:", font=font).grid(row=1, column=0, padx=(20, 0), sticky='e')
        self.class_var = tk.StringVar(value="Select your desired classroom")
        classes_id = list(self.config_manager.load_config().keys())
        self.dropDownMenu = ttk.OptionMenu(self.top, self.class_var, self.class_var.get(), *classes_id)
        self.dropDownMenu.grid(row=1, column=1, sticky='w', padx=(20, 20), pady=(20, 20))

        # Entry for anchor image path with browse button
        ttk.Label(self.top, text="Anchor Image Path:", font=font).grid(row=2, column=0, pady=(0, 20), sticky='e')
        self.anchor_image_path_entry = ttk.Entry(self.top, font=font)
        self.anchor_image_path_entry.grid(row=2, column=1, pady=(0, 20), padx=20, sticky='ew')
        self.anchor_image_path_btn = ttk.Button(self.top, text="Browse", command=self.browse_anchor)
        self.anchor_image_path_btn.grid(row=2, column=2, pady=(0, 20), padx=(0, 20), sticky='w')

        # Process button
        self.process_button = ttk.Button(self.top, text="Process", command=self.process, state='disabled')
        self.process_button.grid(row=3, column=0, columnspan=3, pady=20, sticky='ew')

        # Make middle column expand more to fill space for the entry
        self.top.grid_columnconfigure(1, weight=3)

    def browse_anchor(self):
        self.top.attributes('-topmost', False)  # Keep window on top

        self.anchor_image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])

        self.top.attributes('-topmost', True)  # Keep window on top

        if self.anchor_image_path:
            self.anchor_image_path_entry.delete(0, tk.END)
            self.anchor_image_path_entry.insert(0, self.anchor_image_path)
            self.anchor_image_path_btn.config(state="readonly")

    def load_attributes(self, class_id):
        try:
            class_config = self.config_manager.get_class_config(class_id)
            self.directory_path, self.file_path = class_config.values()
            return True
        except ValueError:
            messagebox.showerror("Configuration Error", "Invalid configuration for the selected class.")
            return False

    def load_file(self):
        """Load or initialize the DataFrame."""
        if os.path.isfile(self.file_path):
            self.df = pd.read_excel(self.file_path, index_col=0)
            # Convert all column names to datetime objects and back to strings for uniform formatting
            self.df.columns = pd.to_datetime(self.df.columns).strftime("%Y-%m-%d")
        else:
            self.initialize_dataframe_from_directory()

    def initialize_dataframe_from_directory(self):
        """Initialize DataFrame with image file names from the directory."""
        file_names = [
            filename.replace("_", " ")[:filename.rindex(".")].strip().capitalize()
            for filename in sorted(os.listdir(self.directory_path), key=lambda label: ord(label[0]))
            if filename.lower().endswith(('.png', '.jpg', '.jpeg'))
        ]

        if not file_names:
            raise FileExistsError("No image files found in the directory.")

        self.df = pd.DataFrame(index=file_names)

    def process(self):
        if not self.load_attributes(self.class_var.get()):
            return

        try:
            self.load_file()
        except PermissionError:
            messagebox.showerror("PermissionError", "Attendance updated Failed.\n please close the excel file and try again")
            return
        
        if not all([hasattr(self, 'directory_path'), hasattr(self, 'anchor_image_path'), hasattr(self, 'file_path')]):
            messagebox.showerror("Error", "Please ensure all paths are set.")
            return

        # Assume FaceRecognitionManager and other methods are defined as before
        self.face_manager = FaceRecognitionManager(self.directory_path, self.anchor_image_path, self.file_path)
        cropped_faces = self.face_manager.crop_faces()
        results = self.face_manager.compare_faces(cropped_faces)
        self.face_manager.update_dataframe(results, self.df)
        
        messagebox.showinfo("Success", "Attendance updated successfully.")

        self.master.destroy()
        if self.callback:
            self.callback(self.file_path)



if __name__ == "__main__":
    root = tk.Tk()
    app = RecognitionWindow(root)
    root.mainloop()