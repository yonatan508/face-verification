import tkinter as tk
from screeninfo import get_monitors

class ApplicationPosition:
    def __init__(self, master, delay=200):
        self.master = master
        self.delay = delay

    @property
    def main_display(self):
        """Returns the primary monitor's information."""
        for monitor in get_monitors():
            if monitor.is_primary:
                return monitor

    def get_app_dimensions(self):
        """Returns the dimensions of the Tkinter window."""
        return self.master.winfo_width(), self.master.winfo_height()

    def get_position(self, width, height):
        """Calculates the coordinates to center the window."""
        center_x = int(self.main_display.x + (self.main_display.width / 2 - width / 2))
        center_y = int(self.main_display.y + (self.main_display.height / 2 - height / 2))
        return center_x, center_y

    def _update_geometry(self):
        """Private method that updates the window's geometry."""
        width, height = self.get_app_dimensions()
        center_x, center_y = self.get_position(width=width, height=height)
        self.master.geometry(f"{width}x{height}+{center_x}+{center_y}")

    def center_window(self):
        """Public method to center the window after a short delay."""
        self.master.after(self.delay, self._update_geometry)
