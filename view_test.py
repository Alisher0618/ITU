import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class PaintView(Gtk.Window):
    def __init__(self, controller):
        super().__init__(title="Paint App")
        self.set_default_size(1920, 1000)
        self.controller = controller
         # Переключение в полноэкранный режим
        #self.fullscreen()

        # Создаем заголовочную панель
        header = Gtk.HeaderBar()
        header.set_show_close_button(True)       # Показывает кнопку закрытия
        header.props.title = "Paint App"         # Заголовок
        self.set_titlebar(header)                # Устанавливаем header как заголовок окна

        # Добавляем кнопки в заголовок
        save_button = Gtk.Button(label="Сохранить")
        save_button.connect("clicked", self.on_save_button_clicked)
        header.pack_end(save_button)             # Кнопка справа

        open_button = Gtk.Button(label="Открыть")
        open_button.connect("clicked", self.on_open_button_clicked)
        header.pack_start(open_button)           # Кнопка слева
        
        self.color_palette =  [
            ("Black", Gdk.RGBA(0, 0, 0, 1)),
            ("White", Gdk.RGBA(1, 1, 1, 1)),
            ("Red", Gdk.RGBA(1, 0, 0, 1)),
            ("Green", Gdk.RGBA(0, 1, 0, 1)),
            ("Blue", Gdk.RGBA(0, 0, 1, 1)),
            ("Yellow", Gdk.RGBA(1, 1, 0, 1)),
            ("Cyan", Gdk.RGBA(0, 1, 1, 1)),
            ("Magenta", Gdk.RGBA(1, 0, 1, 1)),
            ("Gray", Gdk.RGBA(0.5, 0.5, 0.5, 1)),
            ("Orange", Gdk.RGBA(1, 0.65, 0, 1)),
            ("Pink", Gdk.RGBA(1, 0.75, 0.8, 1)),
            ("Purple", Gdk.RGBA(0.5, 0, 0.5, 1)),
            ("Brown", Gdk.RGBA(0.6, 0.3, 0, 1)),
            ("Maroon", Gdk.RGBA(0.5, 0, 0, 1)),
            ("Olive", Gdk.RGBA(0.5, 0.5, 0, 1)),
            ("Navy", Gdk.RGBA(0, 0, 0.5, 1)),
            ("Teal", Gdk.RGBA(0, 0.5, 0.5, 1)),
            ("Lime", Gdk.RGBA(0.75, 1, 0, 1)),
            ("Indigo", Gdk.RGBA(0.29, 0, 0.51, 1)),
            ("Violet", Gdk.RGBA(0.56, 0, 1, 1)),
            ("Gold", Gdk.RGBA(1, 0.84, 0, 1)),
            ("Salmon", Gdk.RGBA(0.98, 0.5, 0.45, 1)),
            ("Coral", Gdk.RGBA(1, 0.5, 0.31, 1)),
            ("Khaki", Gdk.RGBA(0.76, 0.69, 0.57, 1)),
            ("Crimson", Gdk.RGBA(0.86, 0.08, 0.24, 1)),
            ("Turquoise", Gdk.RGBA(0.25, 0.88, 0.82, 1)),
            ("Lavender", Gdk.RGBA(0.9, 0.9, 0.98, 1)),
            ("Beige", Gdk.RGBA(0.96, 0.96, 0.86, 1)),
        ]

    
        self.color_buttons = {}
        
        # Main horizontal box to contain left, center, and right sections
        main_box = Gtk.Box(spacing=0)
        main_box.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 0, 0, 0.2))  # Light gray
        self.add(main_box)
        
        main_grid = Gtk.Grid()        
        
        # Left Panel: Color palette and color picker
        left_panel = Gtk.Box(spacing=0)
        left_panel.set_size_request(200, 1030)
        left_panel.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1, 1, 1, 1))  # Light gray
        left_panel.get_style_context().add_class("left-panel")
    
        main_grid.attach(left_panel, 0, 0, 1, 206)
        
        
        
        
        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5) 
        
        columns = 4
        tmp_row = 0
        tmp_col = 0
        for i, (color_name, color) in enumerate(self.color_palette):
            row = i // columns
            col = i % columns
            color_button = Gtk.Button()
            
            area = Gtk.DrawingArea()
            area.set_size_request(24, 24)  # Size of the color rectangle
            area.connect("draw", self.controller.fill_button, {"color": color})  # Draw the color rectangle
            color_button.add(area)
            
            color_button.set_name(color_name.lower())  # Set a name for CSS styling
            color_button.get_style_context().add_class(color_name)
            color_button.connect("clicked", self.on_color_button_clicked, color)
                
            grid.attach(color_button, col, row, 1, 1)  # Attach button to grid
            self.color_buttons[color_name.lower()] = color_button  # Save button reference
            
            tmp_row = row
            tmp_col = col
            
            
        left_panel.pack_start(grid, False, False, 0)
        
        # Custom color picker in left panel
        color_button = Gtk.ColorButton()
        color_button.set_rgba(controller.get_color())  # Fetch the color from the controller
        color_button.connect("color-set", self.controller.on_color_set)
        color_button.set_margin_top(100)
        grid.attach(color_button, tmp_col-3, tmp_row+2, 4, 1)
        
        # Top Panel: Tools
        top_panel = Gtk.Box(spacing=0)
        top_panel.set_size_request(1690, 50)
        top_panel.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1, 1, 1, 1))
        top_panel.get_style_context().add_class("top-box")
        
        main_grid.attach(top_panel, 1, 0, 338, 9)
        
        central_panel = Gtk.Box(spacing=0)
        central_panel.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1, 1, 1, 1))
        central_panel.get_style_context().add_class("central-box")
        main_grid.attach(central_panel, 2, 10, 338, 196)
        
        # Center Panel: Drawing Area
        self.drawing_area = Gtk.DrawingArea()
        self.drawing_area.get_style_context().add_class("draw-box")
        
        self.drawing_area.set_events(
            Gdk.EventMask.BUTTON_PRESS_MASK |
            Gdk.EventMask.BUTTON_RELEASE_MASK |
            Gdk.EventMask.POINTER_MOTION_MASK
        )
        self.drawing_area.connect("draw", self.controller.on_draw)
        self.drawing_area.connect("button-press-event", self.controller.on_button_press)
        self.drawing_area.connect("button-release-event", self.controller.on_button_release)
        self.drawing_area.connect("motion-notify-event", self.controller.on_mouse_move)
        
        main_grid.attach(self.drawing_area, 3, 11, 335, 194)
        
        
        #END OF GRID
        main_box.pack_start(main_grid, False, False, 0)
        
        
        """grid1 = Gtk.Grid()
        grid1.set_row_spacing(5)
        grid1.set_column_spacing(5) 
        
        button1 = Gtk.Button(label="1")
        button2 = Gtk.Button(label="2")
        button3 = Gtk.Button(label="3")
        button4 = Gtk.Button(label="4")
        button5 = Gtk.Button(label="5")
    
        grid1.add(button1)
        grid1.attach(button2, 1, 0, 1, 1)
        grid1.attach(button3, 2, 0, 1, 1)
        grid1.attach(button4, 0, 1, 1, 1)
        grid1.attach_next_to(button5, button2, Gtk.PositionType.BOTTOM, 2, 1)
        
        top_panel.pack_start(grid1, False, False, 0)"""

        
        """button1 = Gtk.Button(label="1")
        button2 = Gtk.Button(label="2")
        button3 = Gtk.Button(label="3")
        button4 = Gtk.Button(label="4")
        button5 = Gtk.Button(label="5")
    
        grid.add(button1)
        grid.attach(button2, 1, 0, 1, 1)
        grid.attach(button3, 2, 0, 1, 1)
        grid.attach(button4, 0, 1, 1, 1)
        grid.attach_next_to(button5, button2, Gtk.PositionType.BOTTOM, 2, 1)"""
        #color_palette_grid.attach(button3, 1, 1, 1, 1)
        
       
        
        #left_box = Gtk.Box(spacing=0)
        #left_panel.pack_start(left_box, False, False, 50)
        
        
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(b"""
            .left-panel {
                border: 5px solid gray;
                border-radius: 10px;
                background-color: #d3d3d3;
                padding: 10px;                
            }
            
            .top-box {
                border: 5px solid gray;
                margin-left: 5px;
                border-radius: 10px;
                background-color: #d3d3d3;
                padding: 10px;
            }
            
            .central-box {
                border: 5px solid gray;
                border-radius: 10px;
                background-color: #d3d3d3;
                padding: 10px;
            }
        
            
        """)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        
        self.add_css()
        
    def add_css(self):
        css_provider = Gtk.CssProvider()
        screen = Gdk.Screen.get_default()
        css_provider.load_from_data(b"""
        button {
            border-style: solid;
            border-width: 2px;
        }
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
        css_data = b"""
            .dotted-border {
                border: 2px solid black;
            }
        """
        css_provider.load_from_data(css_data)
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

        #css_provider = Gtk.CssProvider()
        for i in enumerate(self.color_palette):
            if color == i[1][1]:
                print("clicked:", i[1][0])
                break
            

    def on_save_button_clicked(self, button):
        print("Сохранение изображения...")

    def on_open_button_clicked(self, button):
        print("Открытие изображения...")

    def queue_draw(self):
        """Request redraw of the drawing area."""
        self.drawing_area.queue_draw()
        