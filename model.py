import gi
from gi.repository import Gdk

class PaintModel:
    def __init__(self):
        self.lines = []  # Each line is a tuple of (points, color, brush_size)
        self.dline = []
        self.current_line = []
        self.delete_line = []
        
        self.draw_or_delete = 0
        self.color = Gdk.RGBA(0, 0, 0, 1)  # Default color: black
        self.rubber_color = Gdk.RGBA(1, 1, 1, 1)
        self.brush_size = 5  # Default brush size
        self.rubber_size = 5
        self.pencil = 0
        
    def on_draw(self, cr):
        """Draw all lines and the current line."""
        #if(self.pencil == 1 and self.draw_or_delete == 0):
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
            if(self.pencil == 1 and self.draw_or_delete == 0):
                cr.set_source_rgba(self.color.red, self.color.green, self.color.blue, self.color.alpha)
                cr.set_line_width(self.brush_size)
            else:
                cr.set_source_rgba(self.rubber_color.red, self.rubber_color.green, self.rubber_color.blue, self.rubber_color.alpha)
                cr.set_line_width(self.rubber_size)

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
            if(self.pencil == 1 and self.draw_or_delete == 0):
                self.lines.append((self.current_line, self.color, self.brush_size))
            else:
                self.lines.append((self.current_line, self.rubber_color, self.rubber_size))
            self.current_line = []
     
    #
    # DELETING LINES
    #       
    #######################################
    """def start_delete_line(self, x, y):
        print(x, y)
        self.delete_line = [(x, y)]
        
    def end_delete_line(self, x, y):
        if self.delete_line:
            self.delete_line.append((x, y))
            self.lines.append((self.delete_line, self.rubber_size, self.rubber_size))
            self.delete_line = []
            
    def add_delete_point(self, x, y):
        if self.delete_line is not None:
            self.delete_line.append((x, y))"""
    ########################################

    def set_color(self, color):
        """Set the brush color."""
        self.color = color
        
    def get_color(self):
        """Return the current color."""
        return self.color

    def set_brush_size(self, size):
        """Set the brush size."""
        print("size of brush:", size)
        self.brush_size = size
        
    def set_rubber_size(self, size):
        """Set the brush size."""
        print("size of rubber:", size)
        self.rubber_size = size

    def get_lines(self):
        """Return all saved lines for drawing."""
        #print("LINE:", self.lines)
        return self.lines
    
    
    def orientation(self, p, q, r):
        """Возвращает ориентацию трех точек (p, q, r).
        0 -> коллинеарны
        1 -> по часовой стрелке
        2 -> против часовой стрелки
        """
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0
        elif val > 0:
            return 1
        else:
            return 2

    def on_segment(self, p, q, r):
        """Проверяет, лежит ли точка q на отрезке pr."""
        if min(p[0], r[0]) <= q[0] <= max(p[0], r[0]) and min(p[1], r[1]) <= q[1] <= max(p[1], r[1]):
            return True
        return False

    def segments_intersect(self, p1, q1, p2, q2):
        """Проверяет пересекаются ли два отрезка (p1, q1) и (p2, q2)"""
        # Определяем ориентации
        o1 = self.orientation(p1, q1, p2)
        o2 = self.orientation(p1, q1, q2)
        o3 = self.orientation(p2, q2, p1)
        o4 = self.orientation(p2, q2, q1)

        # Основной случай
        if o1 != o2 and o3 != o4:
            return True

        # Особые случаи (когда точки коллинеарны)
        # p1, q1 и p2 коллинеарны и p2 лежит на отрезке p1q1
        if o1 == 0 and self.on_segment(p1, p2, q1):
            return True

        # p1, q1 и q2 коллинеарны и q2 лежит на отрезке p1q1
        if o2 == 0 and self.on_segment(p1, q2, q1):
            return True

        # p2, q2 и p1 коллинеарны и p1 лежит на отрезке p2q2
        if o3 == 0 and self.on_segment(p2, p1, q2):
            return True

        # p2, q2 и q1 коллинеарны и q1 лежит на отрезке p2q2
        if o4 == 0 and self.on_segment(p2, q1, q2):
            return True

        # Иначе отрезки не пересекаются
        return False
    
    def clear_canvas(self):
        """Clear all points from the canvas."""
        """print(self.lines)
        print("===================================")
        print(self.dline)
        print("===================================")
        print(self.lines[0][0][0], self.dline[0][0][0], self.lines[0][0][len(self.lines[0][0]) - 1], self.dline[0][0][len(self.dline[0][0]) - 1])
        
        print(self.start_delete_line)
        
        bruh = self.segments_intersect(self.lines[0][0][0], self.lines[0][0][len(self.lines[0][0]) - 1], self.dline[0][0][0], self.dline[0][0][len(self.dline[0][0]) - 1])
        
        for k in self.lines:
            for c1, c2 in zip(k[0], k[0][1:]):
                print(c1, c2)
            
        for l1, l2 in zip(self.lines, self.dline):
                
        
        for k in self.lines:
            for i in range(0, len(k[0]) - 1, 2):
                if i + 1 < len(k[0]):
                    print("Couple:", k[0][i], k[0][i+1])
                
        
        print("Отрезки пересекаются?" , bruh)  # False
        
        if bruh is True:
            
            del self.dline[0]
        """
        
        self.lines = []
