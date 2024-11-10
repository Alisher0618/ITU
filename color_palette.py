# color_palette.py
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class ColorPalette(Gtk.DrawingArea):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.set_size_request(150, -1)  # Fixed width for color panel
        self.connect("draw", self.on_draw_colors)
        self.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.connect("button-press-event", self.on_color_button_clicked)

    def on_draw_colors(self, widget, cr):
        colors = self.controller.get_colors()  # Get colors from controller
        button_height = 40
        for i, (name, color) in enumerate(colors):
            # Set the color and draw the rectangle for the button
            cr.set_source_rgba(color.red, color.green, color.blue, color.alpha)
            cr.rectangle(10, 10 + i * (button_height + 5), 130, button_height)
            cr.fill()
            # Draw the border
            cr.set_source_rgba(0, 0, 0, 1)  # Black border
            cr.rectangle(10, 10 + i * (button_height + 5), 130, button_height)
            cr.stroke()

    def on_color_button_clicked(self, widget, event):
        # Determine which color was clicked based on mouse position
        button_height = 40
        colors = self.controller.get_colors()
        for i, (name, color) in enumerate(colors):
            if 10 + i * (button_height + 5) <= event.y <= 10 + i * (button_height + 5) + button_height:
                self.controller.set_color(color)  # Set the color in the controller
                break
        self.queue_draw()  # Request redraw to reflect any changes
