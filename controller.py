import cairo

class PaintController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def on_draw(self, widget, cr):
        """Draw all lines and the current line."""
        if(self.model.pencil == 1):
            self.model.on_draw(cr)
        else:
            return
        
            
    def fill_button(self, area, cr, user_data):
        self.model.fill_button(area, cr, user_data)

    def on_button_press(self, widget, event):
        """Start drawing a line."""
        if(self.model.pencil == 1):
            if event.button == 1:  # Left mouse button
                self.model.start_line(event.x, event.y)
                self.view.queue_draw()
        else:
            return

    def on_button_release(self, widget, event):
        """Finish drawing a line."""
        if(self.model.pencil == 1):
            if event.button == 1:  # Left mouse button
                self.model.end_line(event.x, event.y)
                self.view.queue_draw()
        else:
            return

    def on_mouse_move(self, widget, event):
        """Draw as the mouse moves."""
        if(self.model.pencil == 1):
            if self.model.current_line:
                self.model.add_point(event.x, event.y)
                self.view.queue_draw()
        else:
            return

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
    
    def clicked_pencil(self, value):
        if(self.model.pencil == 1):
            if(value != "pencil"):
                self.model.pencil = 0
        else:
            self.model.pencil = 1