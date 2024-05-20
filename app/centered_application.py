from screeninfo import get_monitors

class ApplicationPosition:
    def __init__(self, master, delay=200):
        # Initialize with the Tkinter master window and an optional delay for positioning
        self.master = master
        self.delay = delay  # Delay in milliseconds before centering the window

    @property
    def main_display(self):
        """Returns the primary monitor's information using screeninfo library.
        Iterates through all monitors and returns the first one that is marked as primary."""
        for monitor in get_monitors():
            if monitor.is_primary:
                return monitor

    def get_app_dimensions(self):
        """Returns the dimensions of the Tkinter window."""
        # Fetches the current width and height of the master window
        return self.master.winfo_width(), self.master.winfo_height()

    def get_position(self, width, height):
        """Calculates the coordinates to center the window on the screen.
        Uses the dimensions of the primary monitor and the application to calculate the center position."""
        center_x = int(self.main_display.x + (self.main_display.width / 2 - width / 2))
        center_y = int(self.main_display.y + (self.main_display.height / 2 - height / 2))
        return center_x, center_y  # Returns the calculated coordinates

    def _update_geometry(self):
        """Private method that updates the window's geometry to center it.
        It's called after a delay set in the initializer."""
        width, height = self.get_app_dimensions()  # Get current dimensions of the window
        center_x, center_y = self.get_position(width=width, height=height)  # Calculate center position
        # Update the geometry of the master window to position it at the calculated coordinates
        self.master.geometry(f"{width}x{height}+{center_x}+{center_y}")

    def center_window(self):
        """Public method to center the window.
        It waits for the specified delay before updating the window's geometry to ensure dimensions are stable."""
        self.master.after(self.delay, self._update_geometry)  # Schedule the geometry update after the specified delay
