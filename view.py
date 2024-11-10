import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class PaintView(Gtk.Window):
    def __init__(self, controller):
        super().__init__(title="Paint App")
        self.set_default_size(1200, 800)
        self.controller = controller

        # Main horizontal box to contain left, center, and right sections
        main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        #main_box.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1, 0, 0, 1))  # Light gra
        self.add(main_box)

        # Left Panel: Color palette and color picker
        left_panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        left_panel.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0.8, 0.8, 0.8, 1))  # Light gray
        main_box.pack_start(left_panel, False, False, 10)

        # Color palette section in left panel
        self.color_palette = [
            ("Black", Gdk.RGBA(0, 0, 0, 1)),
            ("Red", Gdk.RGBA(1, 0, 0, 1)),
            ("Green", Gdk.RGBA(0, 1, 0, 1)),
            ("Blue", Gdk.RGBA(0, 0, 1, 1)),
            ("Yellow", Gdk.RGBA(1, 1, 0, 1)),
            ("Purple", Gdk.RGBA(0.5, 0, 0.5, 1)),
        ]
        
         # Add color buttons in a Grid layout
        self.color_buttons = {}
        color_palette_grid = Gtk.Grid(column_spacing=5, row_spacing=5)
        color_palette_grid.set_margin_start(10)
        color_palette_grid.set_margin_end(10)
        color_palette_grid.set_margin_top(10)
        color_palette_grid.set_margin_bottom(10)

        # Populate the grid with color buttons
        columns = 2
        for idx, (color_name, color) in enumerate(self.color_palette):
            row = idx // columns
            col = idx % columns
            color_button = Gtk.Button()
            area = Gtk.DrawingArea()
            area.set_size_request(24, 24)  # Size of the color rectangle
            area.connect("draw", self.controller.fill_button, {"color": color})  # Draw the color rectangle
            color_button.add(area)
            color_button.set_name(color_name.lower())  # Set a name for CSS styling
            color_button.connect("clicked", self.on_color_button_clicked, color)
            color_palette_grid.attach(color_button, col, row, 1, 1)  # Attach button to grid
            self.color_buttons[color_name.lower()] = color_button  # Save button reference

        left_panel.pack_start(color_palette_grid, False, False, 10)

        # Custom color picker in left panel
        color_button = Gtk.ColorButton()
        color_button.set_rgba(controller.get_color())  # Fetch the color from the controller
        color_button.connect("color-set", self.controller.on_color_set)
        left_panel.pack_start(color_button, False, False, 10)

        # Center Panel: Drawing Area
        self.drawing_area = Gtk.DrawingArea()
        self.drawing_area.set_size_request(800, 800)
        self.drawing_area.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1, 1, 1, 1))  # White
        self.drawing_area.set_events(
            Gdk.EventMask.BUTTON_PRESS_MASK |
            Gdk.EventMask.BUTTON_RELEASE_MASK |
            Gdk.EventMask.POINTER_MOTION_MASK
        )
        self.drawing_area.connect("draw", self.controller.on_draw)
        self.drawing_area.connect("button-press-event", self.controller.on_button_press)
        self.drawing_area.connect("button-release-event", self.controller.on_button_release)
        self.drawing_area.connect("motion-notify-event", self.controller.on_mouse_move)
        main_box.pack_start(self.drawing_area, True, True, 0)

        # Right Panel: Tools
        right_panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        right_panel.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0.8, 0.8, 0.8, 1))  # Light gray

        main_box.pack_start(right_panel, False, False, 10)

        # Brush size slider in right panel
        brush_size_adjustment = Gtk.Adjustment(5, 1, 50, 1, 1, 0)
        brush_size_slider = Gtk.Scale(orientation=Gtk.Orientation.VERTICAL, adjustment=brush_size_adjustment)
        brush_size_slider.set_value(controller.get_brush_size())
        brush_size_slider.connect("value-changed", self.controller.on_brush_size_changed)
        right_panel.pack_start(brush_size_slider, True, True, 10)

        # Clear button
        clear_button = Gtk.Button(label="Clear Canvas")
        clear_button.connect("clicked", self.controller.on_clear_canvas)
        right_panel.pack_start(clear_button, False, False, 10)

        # Load CSS
        #self.add_css()

    def add_css(self):
        css_provider = Gtk.CssProvider()
        screen = Gdk.Screen.get_default()
        css_provider.load_from_data(b"""
        button {
            border: 2px solid #000;  /* Black border */
            border-radius: 5px;      /* Rounded corners */
            padding: 5px;            /* Padding inside buttons */
        }
        button#black { border: 4px solid #000; border-color: black; color: black;}
        button#red { border: 4px solid #000; border-color: red; color: red;}
        button#green { border: 4px solid #000; border-color: green; color: green;}
        button#blue { border: 4px solid #000; border-color: blue; color: blue;}
        button#yellow { border: 4px solid #000; border-color: yellow; color: yellow;}
        button#purple { border: 4px solid #000; border-color: purple; color: purple;}
        """)
        
        
        Gtk.StyleContext.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

    def on_color_button_clicked(self, button, color):
        """Handle color button clicks to set the brush color."""
        self.controller.set_color(color)
        
        # Reset all button borders
        for name, btn in self.color_buttons.items():
            btn.get_style_context().remove_class("dotted-border")
        
        # Apply dotted border to the clicked button
        button.get_style_context().add_class("dotted-border")

        # Update CSS for dotted border

        css_provider = Gtk.CssProvider()
        if(color == Gdk.RGBA(0, 0, 0, 1)):
            css_provider = Gtk.CssProvider()
            css_provider.load_from_data(b"""
            button#black.dotted-border { border: 4px dotted #000; border-color: black; }
            """)
        elif(color == Gdk.RGBA(1, 0, 0, 1)):
            css_provider = Gtk.CssProvider()
            css_provider.load_from_data(b"""
            button#red.dotted-border { border: 4px dotted #000; border-color: red; }
            """)
        elif(color == Gdk.RGBA(0, 1, 0, 1)):
            css_provider = Gtk.CssProvider()
            css_provider.load_from_data(b"""
            button#green.dotted-border { border: 4px dotted #000; border-color: green; }
            """)
        elif(color == Gdk.RGBA(0, 0, 1, 1)):
            css_provider = Gtk.CssProvider()
            css_provider.load_from_data(b"""
            button#blue.dotted-border { border: 4px dotted #000; border-color: blue; }
            """)
        elif(color == Gdk.RGBA(1, 1, 0, 1)):
            css_provider = Gtk.CssProvider()
            css_provider.load_from_data(b"""
            button#yellow.dotted-border { border: 4px dotted #000; border-color: yellow; }
            """)
        elif(color == Gdk.RGBA(0.5, 0, 0.5, 1)):
            css_provider = Gtk.CssProvider()
            css_provider.load_from_data(b"""
            button#purple.dotted-border { border: 4px dotted purple; border-color: purple; }
            """)
            
        #css_provider.load_from_data(b"""
        #button.dotted-border {
        #    border: 4px dotted black;  /* Dotted border for selected button */
        #}
        #""")
        
        screen = Gdk.Screen.get_default()
        Gtk.StyleContext.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

    def queue_draw(self):
        """Request redraw of the drawing area."""
        self.drawing_area.queue_draw()
