'''
    View.py
    Author: Alisher Mazhirinov, xmazhi00
    Model for DrawEasy application
'''

import gi
from gi.repository import Gdk
import cairo
import json


class PaintModel:
    def __init__(self):
        self.image_surface = None
        
        #self.tmp_lines = []
        self.operations = []
        
        self.lines = []  # Each line is a tuple of (points, color, brush_size)
        self.str_line = []
        
        self.clicked_clear = False

        self.current_line = []
        #self.delete_line = []
        
        self.selected_line_index = None
        self.move_offset = None
        
        self.advanced_rubber = False
        
        self.straight_line = []
        self.start_point = []
        self.end_point = []
        
        self.draw_or_delete = 0
        self.color = Gdk.RGBA(0, 0, 0, 1)
        self.rubber_color = Gdk.RGBA(1, 1, 1, 1)
        self.new_line =  Gdk.RGBA(1, 0, 0, 1)
        self.brush_size = 5
        self.rubber_size = 5
        self.line_size = 3
        self.brush = 1
        self.draw_lines = 0
        
        self.grid_visible = False 
        
        self.is_save = False
        self.saved_path = ""
        self.saved_format = ""
        self.is_loaded = False
    
    ##################################################################################
    #   DRAWING                                                                      #
    ##################################################################################
    def on_draw(self, cr):
        """Draw all lines and the current line."""   
        
        for line, color, size in self.get_lines():
            cr.set_source_rgba(color.red, color.green, color.blue, color.alpha)
            cr.set_line_width(size)
            cr.move_to(line[0][0], line[0][1])
            for point in line[1:]:
                cr.line_to(point[0], point[1])
            cr.stroke()
        
        if self.current_line:
            if(self.draw_lines == 0):
                if(self.brush == 1 and self.draw_or_delete == 0):
                    cr.set_source_rgba(self.color.red, self.color.green, self.color.blue, self.color.alpha)
                    cr.set_line_width(self.brush_size)
                elif(self.brush == 0 and self.draw_or_delete == 1):
                    cr.set_source_rgba(self.rubber_color.red, self.rubber_color.green, self.rubber_color.blue, self.rubber_color.alpha)
                    cr.set_line_width(self.rubber_size) 
                    
                cr.move_to(self.current_line[0][0], self.current_line[0][1])
                for point in self.current_line[1:]:
                    cr.line_to(point[0], point[1])
                cr.stroke()
            
            else:
                cr.set_source_rgba(self.color.red, self.color.green, self.color.blue, self.color.alpha)
                cr.set_line_width(self.line_size)
                cr.move_to(self.current_line[0][0], self.current_line[0][1])
                cr.line_to(self.end_point[0], self.end_point[1])
                self.end_point = []
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
            
            if(self.brush == 1 and self.draw_or_delete == 0 and self.draw_lines == 0):
                self.lines.append((self.current_line, self.color, self.brush_size))
                self.operations.append((self.current_line, self.color, self.brush_size))
            elif(self.brush == 0 and self.draw_or_delete == 1 and self.draw_lines == 0):
                self.lines.append((self.current_line, self.rubber_color, self.rubber_size))
                self.operations.append((self.current_line, self.color, self.brush_size))
            elif(self.brush == 0 and self.draw_or_delete == 0 and self.draw_lines == 1):
                self.lines.append((self.current_line, self.color, self.line_size))
                self.operations.append((self.current_line, self.color, self.line_size))
            self.is_save = False
            self.current_line = []
            
    def end_straight_line(self, x, y):
        """End drawing straight line"""
        if self.start_point:
            self.straight_line.append([x, y])
            self.lines.append((self.straight_line[0], self.color, self.line_size))
            self.operations.append((self.straight_line[0], self.color, self.line_size))
            self.is_save = False
            self.straight_line = []
            
    def find_line_near_point(self, x, y, threshold=5):
        """Find line near point."""
        for index, (line, color, size) in enumerate(self.lines):
            for i in range(len(line) - 1):
                if self.is_point_near_line((x, y), line[i], line[i + 1], threshold):
                    return index
        
        return None

    def is_point_near_line(self, point, start, end, threshold):
        """Check if a point is near a line."""
        px, py = point
        x1, y1 = start
        x2, y2 = end

        dx, dy = x2 - x1, y2 - y1
        if dx == 0 and dy == 0:
            return abs(px - x1) <= threshold and abs(py - y1) <= threshold

        t = max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / (dx**2 + dy**2)))
        nearest_x = x1 + t * dx
        nearest_y = y1 + t * dy
        dist = ((px - nearest_x)**2 + (py - nearest_y)**2)**0.5
        return dist <= threshold

    def select_line_at_point(self, x, y):
        """Select line at point."""
        self.selected_line_index = self.find_line_near_point(x, y)

    def move_line(self, x, y):
        """Move the selected line to a new location."""
        if self.selected_line_index is not None and self.move_offset is not None:
            line, color, size = self.lines[self.selected_line_index]
            dx, dy = x - self.move_offset[0], y - self.move_offset[1]
            self.lines[self.selected_line_index] = ([(px + dx, py + dy) for px, py in line], color, size)
            self.move_offset = (x, y)
            self.is_save = False

    def delete_lines(self):
        """Delete lines using advanced rubber mode"""
        if self.selected_line_index is not None:
            self.lines.remove(self.lines[self.selected_line_index])
            self.selected_line_index = None
            self.is_save = False
    
    def on_undo_clicked(self):
        """Handle undo function"""
        self.operations.append(self.lines.pop())
        
    def on_redo_clicked(self):
        """Handle redo function"""
        self.lines.append(self.operations.pop())
    ##################################################################################
    
    ##################################################################################
    #   SAVING FUNCTIONS                                                             #
    ##################################################################################
    def set_color(self, color):
        """Set the brush color."""
        self.color = color
        
    def get_color(self):
        """Return the current color."""
        return self.color

    def set_brush_size(self, size):
        """Set the brush size."""
        self.brush_size = size
        
    def set_line_size(self, size):
        """Set the line size."""
        self.line_size = size
        
    def set_rubber_size(self, size):
        """Set the rubber size."""
        self.rubber_size = size

    def get_lines(self):
        """Return all saved lines for drawing."""
        return self.lines
    
    def set_saving_state(self, state):
        self.is_save = state
    
    def get_saving_state(self):
        return self.is_save
    
    def set_saved_path(self, path, type_format):
        self.saved_path = path
        self.saved_format = type_format
    
    def get_saved_path(self):
        return self.saved_path
    
    def set_loaded_state(self, state):
        self.is_loaded = state
    
    def quick_save_canvas(self, allocation):
        if self.saved_format == "png" or self.saved_format == "jpeg":
            self.save_canvas(allocation, self.saved_path)
        else:
            self.save_json(self.saved_path)
        self.is_save = True
    ##################################################################################

    ##################################################################################
    #   SHOW GRID                                                                    #
    ##################################################################################
    def show_grid(self, allocation, cr):
        """Grid"""
        width, height = allocation.width, allocation.height

        # Grid color
        cr.set_source_rgba(0.8, 0.8, 0.8, 0.5) 

        # Draw vertical lines
        for x in range(0, width, 20):
            cr.move_to(x, 0)
            cr.line_to(x, height)
            cr.stroke()

        # Draw horizontal lines
        for y in range(0, height, 20):
            cr.move_to(0, y)
            cr.line_to(width, y)
            cr.stroke()
    ##################################################################################
            
    ##################################################################################
    #   IMPORT AND EXPORT                                                            #
    ##################################################################################
    def save_canvas(self, allocation, file_path):
        """Function to save canvas"""
        width, height = allocation.width, allocation.height

        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        cr = cairo.Context(surface)
        
        if self.image_surface is None:
            cr.set_source_rgb(1, 1, 1)
            cr.rectangle(0, 0, width, height)
            cr.fill()
        else:
            cr.set_source_surface(self.image_surface, 0, 0)
            cr.paint()

        self.on_draw(cr)

        surface.write_to_png(file_path)
        print(f"Canvas saved to {file_path}")
        
    
    def rgba_to_dict(self, rgba):
        """Convert the RGBA object to a dictionary"""
        return {
            "red": rgba.red,
            "green": rgba.green,
            "blue": rgba.blue,
            "alpha": rgba.alpha
        }
                
    def save_json(self, file_path):
        """Convert each row and its RGBA into a serializable format"""
        serializable_lines = [
            (coords, self.rgba_to_dict(rgba), width) for coords, rgba, width in self.lines
        ]
        
        with open(file_path, 'w') as f:
            json.dump(serializable_lines, f, indent=4)
        print(f"Lines saved to {file_path}")
        
    def dict_to_rgba(self, rgba_dict):
        """Convert the dictionary into a Gdk.RGBA object"""
        rgba = Gdk.RGBA()
        rgba.red = rgba_dict["red"]
        rgba.green = rgba_dict["green"]
        rgba.blue = rgba_dict["blue"]
        rgba.alpha = rgba_dict["alpha"]
        return rgba
        
    def open_json(self, file_path):
        """Loading a list of lines from a JSON file.""" 
        with open(file_path, 'r') as f:
            data = json.load(f)
            
        restored_lines = [
            (coords, self.dict_to_rgba(rgba), width) for coords, rgba, width in data
        ]
        for i in restored_lines:
            self.lines.append(i)
        
        print(f"Lines loaded from {file_path}")
    ##################################################################################


    ##################################################################################
    #   CLEAR CANVAS                                                                 #
    ##################################################################################
    def clear_canvas(self):
        """Function to clear canvas"""
        self.lines = []
        self.str_line = []
        self.start_point = []
        self.end_point = []
    ##################################################################################
    