import gi
from gi.repository import Gdk

class PaintModel:
    def __init__(self):
        self.lines = []  # Each line is a tuple of (points, color, brush_size)
        self.current_line = []
        self.color = Gdk.RGBA(0, 0, 0, 1)  # Default color: black
        self.color1 = Gdk.RGBA(0, 0, 0, 1)  # Default color: black
        self.brush_size = 5  # Default brush size
        self.pencil = 0
        
    def on_draw(self, cr):
        """Draw all lines and the current line."""
        if(self.pencil == 1):
            for line, color, size in self.get_lines():
                cr.set_source_rgba(color.red, color.green, color.blue, color.alpha)
                cr.set_line_width(size)
                cr.move_to(line[0][0], line[0][1])
                for point in line[1:]:
                    cr.line_to(point[0], point[1])
                cr.stroke()
                #cr.fill()# - check this nice shit

            # Draw the current line
            if self.current_line:
                cr.set_source_rgba(self.color.red, self.color.green, self.color.blue, self.color.alpha)
                cr.set_line_width(self.brush_size)
                cr.move_to(self.current_line[0][0], self.current_line[0][1])
                for point in self.current_line[1:]:
                    cr.line_to(point[0], point[1])
                cr.stroke()
        
    def fill_button(self, area, cr, user_data):
        """Draw the color rectangle in the button."""
        color = user_data['color']
        cr.set_source_rgba(color.red, color.green, color.blue, color.alpha)
        cr.rectangle(0, 0, 36, 24)  # Rectangle size
        cr.fill()

    def start_line(self, x, y):
        """Start a new line with the current color and brush size."""
        self.current_line = [(x, y)]

    def add_point(self, x, y):
        """Add a point to the current line."""
        if self.current_line is not None:
            self.current_line.append((x, y))

    def end_line(self, x, y):
        """Finish the current line and save it."""
        if self.current_line:
            self.current_line.append((x, y))
            self.lines.append((self.current_line, self.color, self.brush_size))
            self.current_line = []

    def set_color(self, color):
        """Set the brush color."""
        self.color = color
        
    def get_color(self):
        """Return the current color."""
        return self.color

    def set_brush_size(self, size):
        """Set the brush size."""
        self.brush_size = size

    def get_lines(self):
        """Return all saved lines for drawing."""
        return self.lines
    
    def clear_canvas(self):
        """Clear all points from the canvas."""
        self.lines = []
