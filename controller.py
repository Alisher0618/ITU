'''
    View.py
    Author: Alisher Mazhirinov, xmazhi00
    Controller for DrawEasy application
'''

import cairo
from gi.repository import Gdk

class PaintController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.is_drawing = False
        self.checkbutton_mode = "disable"
        self.is_moving_mode = False
    ##################################################################################
    #   DRAWING                                                                      #
    ##################################################################################
    def on_draw(self, widget, cr):
        """Draw all lines and the current line."""
        
        if(self.model.grid_visible is True):
            allocation = self.view.drawing_area.get_allocation()
            self.model.show_grid(allocation, cr)
            
        if(self.model.get_saving_state() is False):
            self.view.label.set_text("Not saved")
        else:
            self.view.label.set_text("Saved")
        
        if self.model.image_surface:
            # Paint the image onto the drawing area (scaling it to fit if needed)
            cr.set_source_surface(self.model.image_surface, 0, 0)
            cr.paint()
           
        self.model.on_draw(cr)
    
    def fill_button(self, area, cr, user_data):
        """Filling with palette buttons"""
        self.model.fill_button(area, cr, user_data)

    def on_button_press(self, widget, event):
        """Start drawing a line."""
        if self.is_moving_mode and event.button == 1:
            self.model.select_line_at_point(event.x, event.y)
            self.model.move_offset = (event.x, event.y)
        elif self.model.advanced_rubber and event.button == 1:
            self.model.select_line_at_point(event.x, event.y)
        elif event.button == 1:  # Left mouse button
            self.model.start_line(event.x, event.y)
            self.view.queue_draw()
        
    def on_button_release(self, widget, event):
        """Finish drawing a line."""
        if self.is_moving_mode:
            self.model.move_offset = None
        elif self.model.advanced_rubber:
            self.view.queue_draw()
        elif event.button == 1:  # Left mouse button
            if(self.model.draw_lines == 0):
                self.model.end_line(event.x, event.y)
                self.view.queue_draw()
            else:
                self.is_drawing = False
                self.model.end_line(event.x, event.y)
                self.view.queue_draw()

    def on_mouse_move(self, widget, event):
        """Draw as the mouse moves."""
        if self.is_moving_mode and self.model.move_offset:
            self.model.move_line(event.x, event.y)
            self.view.queue_draw()
        elif self.model.advanced_rubber:
            self.model.delete_lines()
        else:
            self.is_drawing = True
            if(self.model.draw_lines == 0):
                if self.model.current_line:
                    self.model.add_point(event.x, event.y)
                    self.view.queue_draw()
            else:
                if self.is_drawing:
                    self.model.end_point = (event.x, event.y)
                    self.view.queue_draw()

    def move_objects_mode(self):
        """Reseting values of line index and offset"""
        self.model.selected_line_index = None
        self.model.move_offset = None
        self.view.queue_draw()
    ##################################################################################
        
        
    ##################################################################################
    #   SAVING FUNCTIONS                                                             #
    ##################################################################################          
    def set_saving_state(self, state):
        """Setting saving state(True or False)"""       
        self.model.set_saving_state(state)

    def get_saving_state(self):
        """Getting saving state(True or False)""" 
        return self.model.get_saving_state()
   
    def set_saved_path(self, path, type_format):
        """Setting path for saved file""" 
        self.model.set_saved_path(path, type_format)
        
    def get_saved_path(self):
        """Getting path for saved file""" 
        return self.model.get_saved_path()
    
    def set_loaded_state(self, state):
        """Setting state if image is loaded""" 
        self.model.set_loaded_state(state)

    def quick_save_canvas(self):
        """Quick save if Ctrl+C is pressed"""
        allocation = self.view.drawing_area.get_allocation()
        self.model.quick_save_canvas(allocation)
        self.view.queue_draw()
    ##################################################################################

    def on_color_set(self, widget):
        """Update the brush color from the color button"""
        self.model.set_color(widget.get_rgba())

    def on_brush_size_changed(self, widget):
        """Update the brush size from the slider"""
        self.model.set_brush_size(widget.get_value())
        
    def on_line_size_changed(self, widget):
        """Update the line size from the slider"""
        self.model.set_line_size(widget.get_value())
        
    def on_rubber_size_changed(self, widget):
        """Update the rubber size from the slider"""
        self.model.set_rubber_size(widget.get_value())
        
    def set_color(self, color):
        """Update the brush color directly from the palette"""
        self.model.set_color(color)

    def get_color(self):
        """Get the current color"""
        return self.model.get_color()
    
    def get_color_custom(self):
        """Get the current color of custom palette from the model"""
        return self.model.get_color_custom()

    def get_brush_size(self):
        """Get current brush size"""
        return self.model.brush_size
    
    def get_line_size(self):
        """Get current line size"""
        return self.model.line_size
    
    def get_rubber_size(self):
        """Get current rubber size."""
        return self.model.rubber_size
    
    ##################################################################################
    #   TOOL BUTTONS                                                                 #
    ##################################################################################
    def clicked_brush(self):
        """Set brush drawing mode"""
        self.model.brush = 1
        self.model.draw_or_delete = 0
        self.model.draw_lines = 0
        self.model.advanced_rubber = False
    
    def clicked_rubber(self):
        """Set deleting mode"""
        self.model.brush = 0
        self.model.draw_lines = 0
        self.model.draw_or_delete = 1
        self.set_color(Gdk.RGBA(1, 1, 1, 1))
        if(self.checkbutton_mode == "enable"):
            self.model.advanced_rubber = True
        
    def clicked_straight_lines(self):
        """Set line drawing mode"""
        self.model.brush = 0
        self.model.draw_or_delete = 0
        self.model.draw_lines = 1
        self.model.advanced_rubber = False
        
    def checkbutton_clicked(self, mode):
        """Set or unset the advanced mode of rubber"""
        if self.model.draw_or_delete == 1 and mode == "enable":
            self.model.advanced_rubber = True
            self.checkbutton_mode = "enable"
        else:
            self.model.advanced_rubber = False
            self.checkbutton_mode = "disable"
    
    def show_grid_clicked(self):
        """Set or unset the grid mode"""
        if self.model.grid_visible is False:
            self.model.grid_visible = True
        else:
            self.model.grid_visible = False
        self.view.queue_draw()
    ##################################################################################
    
    
    ##################################################################################
    #   SAVE AND LOAD CANVAS                                                         #
    ##################################################################################       
    def save_canvas(self, file_path, type_format):
        """Save the current canvas to a png, jpeg or json format"""
        if type_format == "png" or type_format == "jpeg":
            allocation = self.view.drawing_area.get_allocation()
            self.model.save_canvas(allocation, file_path)
        else:
            self.model.save_json(file_path)
        
    def load_canvas(self, file_path):
        """Load a PNG file into the canvas as a background image."""
        if(file_path[-4:] == "json"):
            self.model.open_json(file_path)
        else:
            self.model.set_loaded_state(True)
            self.model.image_surface = cairo.ImageSurface.create_from_png(file_path)
            self.view.queue_draw()
    ##################################################################################    
        
    def on_clear_canvas(self, widget):
        """Clear the canvas by removing all points"""
        #self.model.tmp_lines = self.model.lines
        self.model.clicked_clear = True
        self.model.set_saving_state(False)
        self.model.clear_canvas()
        self.model.image_surface = None
        self.view.queue_draw()
            
    def on_undo_clicked(self):
        """Handle undo function"""
        if len(self.model.lines) != 0:
            self.model.on_undo_clicked()
            self.view.queue_draw()
        
    def on_redo_clicked(self):
        """Handle redo function"""
        if len(self.model.operations) != 0:
            self.model.on_redo_clicked()
            self.view.queue_draw()
        
    #def clear_canvas(self):
    #    self.model.set_saving_state(False)
    #    self.model.clear_canvas()
        