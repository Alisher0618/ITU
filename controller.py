import cairo

class PaintController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def on_draw(self, widget, cr):
        self.model.on_draw(cr)
        """Draw all lines and the current line."""
        """for line, color, size in self.model.get_lines():
            cr.set_source_rgba(color.red, color.green, color.blue, color.alpha)
            cr.set_line_width(size)
            cr.move_to(line[0][0], line[0][1])
            for point in line[1:]:
                cr.line_to(point[0], point[1])
            cr.stroke()
            #cr.fill()# - check this nice shit

        # Draw the current line
        if self.model.current_line:
            cr.set_source_rgba(self.model.color.red, self.model.color.green, self.model.color.blue, self.model.color.alpha)
            cr.set_line_width(self.model.brush_size)
            cr.move_to(self.model.current_line[0][0], self.model.current_line[0][1])
            for point in self.model.current_line[1:]:
                cr.line_to(point[0], point[1])
            cr.stroke()
            """
            
    def fill_button(self, area, cr, user_data):
        self.model.fill_button(area, cr, user_data)

    def on_button_press(self, widget, event):
        """Start drawing a line."""
        if event.button == 1:  # Left mouse button
            self.model.start_line(event.x, event.y)
            self.view.queue_draw()

    def on_button_release(self, widget, event):
        """Finish drawing a line."""
        if event.button == 1:  # Left mouse button
            self.model.end_line(event.x, event.y)
            self.view.queue_draw()

    def on_mouse_move(self, widget, event):
        """Draw as the mouse moves."""
        if self.model.current_line:
            self.model.add_point(event.x, event.y)
            self.view.queue_draw()

    def on_color_set(self, widget):
        """Update the brush color from the color button."""
        self.model.set_color(widget.get_rgba())

    def on_brush_size_changed(self, widget):
        """Update the brush size from the slider."""
        self.model.set_brush_size(widget.get_value())

    def set_color(self, color):
        """Update the brush color directly from the palette."""
        self.model.set_color(color)

    def on_clear_canvas(self, widget):
        """Clear the canvas by removing all points."""
        self.model.clear_canvas()
        self.view.queue_draw()
    
    def get_color(self):
        """Get the current color from the model."""
        return self.model.get_color()
    
    def get_color_custom(self):
        """Get the current color from the model."""
        return self.model.get_color_custom()

    def get_brush_size(self):
        """Return current brush size."""
        return self.model.brush_size
