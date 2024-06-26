import os, platform, subprocess

import tkinter as tk
from tkinter.font import Font
from tkinter import messagebox, ttk

# Custom modules for different windows and features in the app
from class_id_setup import ClassIDSetupWindow
from recognition_window import RecognitionWindow
from centered_application import ApplicationPosition
from show_app_info import ApplicationInstructionManual


class MainApplication:
    def __init__(self, master):
        self.master = master
        master.title("Face Recognition Attendance System")
        master.resizable(False, False)

        # Center the primary window
        app_position = ApplicationPosition(self.master)
        app_position.center_window()

        # Set primary window as always topmost initially
        master.attributes("-topmost", True)

        self.setup_ui()

    def setup_ui(self):
        # Configure grid columns
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_columnconfigure(2, weight=1)

        # Set up the title with styling
        title_font = Font(family="Arial", size=16, weight="bold")
        ttk.Label(self.master, text="Face Recognition Attendance System", font=title_font).grid(row=0, column=0, columnspan=3, pady=20)

        # Buttons for different actions
        info_btn = ttk.Button(self.master, text="About the App", command=self.show_app_info)
        info_btn.grid(row=2, column=0, pady=5, padx=20, sticky='ew')

        setup_class_btn = ttk.Button(self.master, text="Setup Class ID", command=self.setup_class_id)
        setup_class_btn.grid(row=2, column=1, pady=5, padx=20, sticky='ew')

        start_recognition_btn = ttk.Button(self.master, text="Start Face Recognition", command=self.start_face_recognition)
        start_recognition_btn.grid(row=2, column=2, pady=5, padx=20, sticky='ew')

    def show_app_info(self):
        # Display the app information window
        self.master.withdraw()
        ApplicationInstructionManual(self, self.master)

    def setup_class_id(self):
        # Open the class ID setup window
        self.master.withdraw()
        ClassIDSetupWindow(self, self.master)

    def start_face_recognition(self):
        # Start the face recognition feature
        self.master.withdraw()
        RecognitionWindow(self.master, self.open_excel_file)

    def rerendering(self, top):
        top.destroy()
        self.master.deiconify()

    def open_excel_file(self, filepath):
        # Opens an Excel file using the appropriate system command
        try:
            if platform.system() == 'Windows':
                os.startfile(filepath)
            elif platform.system() == 'Darwin':
                subprocess.run(['open', filepath])
            else:
                subprocess.run(['xdg-open', filepath])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open Excel file: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()
