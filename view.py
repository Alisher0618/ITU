'''
    View.py
    Author: Alisher Mazhirinov, xmazhi00
    View for DrawEasy application
'''

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf
import os
import sys

class PaintView(Gtk.Window):
    def __init__(self, controller):
        super().__init__(title="Draw Easy")
        self.set_default_size(1920, 972)
        self.controller = controller
        
        self.last_color = None
        self.last_color_button = None
        
        self.color_buttons = {}
        self.tools_button = {}

        # Header Panel
        header = Gtk.HeaderBar()
        header.set_show_close_button(True)
        header.props.title = "Draw Easy"
        self.set_titlebar(header)
        
        # Create a drop-down menu for the "File" button
        file_menu = Gtk.Menu()

        # Create menu items
        new_item = Gtk.MenuItem(label="New")
        open_item = Gtk.MenuItem(label="Open")
        quit_item = Gtk.MenuItem(label="Quit")
        
        # Add handlers for menu items
        new_item.connect("activate", self.on_new_menu_item_clicked)
        open_item.connect("activate", self.on_open_menu_item_clicked)
        quit_item.connect("activate", self.on_quit_menu_item_clicked)
        
        # Save menu in File menu
        save_menu = Gtk.Menu()
        
        save_png = Gtk.MenuItem(label="PNG")
        save_jpeg = Gtk.MenuItem(label="JPEG")
        save_json = Gtk.MenuItem(label="JSON")
        
        save_menu.append(save_png)
        save_menu.append(save_jpeg)
        save_menu.append(save_json)
        
        save_png.connect("activate", lambda widget: self.on_save_menu_item_clicked(widget, "png"))
        save_jpeg.connect("activate", lambda widget: self.on_save_menu_item_clicked(widget, "jpeg"))
        save_json.connect("activate", lambda widget: self.on_save_menu_item_clicked(widget, "json"))
        
        save_menu.show_all()
        
        save_menu_tmp = Gtk.MenuItem(label="Save as...")
        save_menu_tmp.set_submenu(save_menu)  # Set a submenu for this menu item

        # Add items to the menu
        file_menu.append(new_item)
        file_menu.append(open_item)
        file_menu.append(save_menu_tmp)
        file_menu.append(quit_item)
        
        # Show the menu
        file_menu.show_all()

        # Create a button for the HeaderBar and bind the menu
        file_menu_button = Gtk.MenuButton(label="File")
        file_menu_button.set_popup(file_menu)
        header.pack_start(file_menu_button)

        # Repeat for other buttons (eg Edit, Help)
        edit_menu = Gtk.Menu()
        undo_item = Gtk.MenuItem(label="Undo")
        redo_item = Gtk.MenuItem(label="Redo")
        
        self.tools_button["Undo"] = undo_item
        self.tools_button["Redo"] = redo_item
        
        undo_item.connect("activate", self.on_undo_menu_item_clicked)
        redo_item.connect("activate", self.on_redo_menu_item_clicked)
        
        edit_menu.append(undo_item)
        edit_menu.append(redo_item)
        edit_menu.show_all()

        edit_menu_button = Gtk.MenuButton(label="Edit")
        edit_menu_button.set_popup(edit_menu)
        header.pack_start(edit_menu_button)
        
        tips_button = Gtk.Button.new_from_icon_name("dialog-information", Gtk.IconSize.BUTTON)
        tips_button.connect("clicked", self.on_tip_clicked)
        tips_button.set_tooltip_text("Show useful tips")
        header.pack_end(tips_button)
        
        spacer = Gtk.Box()
        spacer.set_size_request(10, -1)  # 10px wide "placeholder"
        header.pack_start(spacer)
        
        self.label = Gtk.Label(label="Not saved")
        header.pack_start(self.label)
        
        #
        #   PALETTE
        #
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

        # Main horizontal box to contain left, center, and right sections
        main_box = Gtk.Box(spacing=0)
        main_box.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 0, 0, 0.2))  # Light gray
        self.add(main_box)
        
        main_grid = Gtk.Grid()
        
        #
        #   TOP PANEL: TOOLS
        #
        top_panel = Gtk.Box(spacing=0)
        top_panel.set_size_request(1696, 50)
        top_panel.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1, 1, 0.8, 1))
        top_panel.get_style_context().add_class("top-box")

        tools_grid = Gtk.Grid(column_spacing=5, row_spacing=5)
        
        #
        #   LEFT PANEL: COLOR PALETTE AND COLOR PICKER
        #
        left_panel = Gtk.Box(spacing=0)
        left_panel.set_size_request(200, 972)
        left_panel.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1, 1, 0.8, 1))
        left_panel.get_style_context().add_class("left-panel")
    
        main_grid.attach(left_panel, 0, 0, 1, 206)
        
        top_panel.pack_start(tools_grid, False, False, 0)
        main_grid.attach(top_panel, 1, 0, 338, 9)
        
        #
        #   CENTRAL PANEL: DRAWING AREA
        #
        central_panel = Gtk.Box(spacing=0)
        central_panel.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1, 1, 1, 1))
        central_panel.get_style_context().add_class("central-box")
        main_grid.attach(central_panel, 2, 10, 338, 196)
        
        
        #
        # PALETTE
        #
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
            if(color_button.get_name() == "black"):
                 color_button.get_style_context().add_class("solid-border")
                 
            color_button.get_style_context().add_class(color_name)
            color_button.connect("clicked", self.on_color_button_clicked, color)
            
            grid.attach(color_button, col, row, 1, 1)  # Attach button to grid
            self.color_buttons[color_name.lower()] = color_button  # Save button reference
            self.last_color_button = color_name.lower()
            tmp_row = row
            tmp_col = col
            
            
        left_panel.pack_start(grid, False, False, 0)
        
        #
        #   CUSTOM COLOR PICKER
        #
        color_button = Gtk.ColorButton()
        color_button.set_rgba(controller.get_color())  # Fetch the color from the controller
        color_button.connect("color-set", self.controller.on_color_set)
        color_button.set_tooltip_text("Pick custom color")
        color_button.set_margin_top(100)
        grid.attach(color_button, tmp_col-3, tmp_row+2, 4, 1)

        #
        #   BRUSH BUTTON
        #
        brush_button = Gtk.Button()

        img = Gtk.Image()
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size("icons/brush.png", 28, 28)
        img.set_from_pixbuf(pixbuf)
        brush_button.set_image(img)
        
        tools_grid.attach(brush_button, 1, 0, 1, 1)
        brush_button.connect("clicked", self.brush_button_clicked)
        brush_button.set_tooltip_text("Pick Brush, Ctrl+B")
        self.tools_button["Brush"] = brush_button
        brush_button.get_style_context().add_class("solid-border")
        
        #
        #   DRAW STRAIGHT BUTTON
        #
        straight_lines_button = Gtk.Button()
        
        img = Gtk.Image()
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size("icons/line.png", 28, 28)
        img.set_from_pixbuf(pixbuf)
        straight_lines_button.set_image(img)
        
        tools_grid.attach(straight_lines_button, 2, 0,1, 1)
        straight_lines_button.connect("clicked", self.draw_lines_clicked)
        straight_lines_button.set_tooltip_text("Draw straight lines, Ctrl+L")
        self.tools_button["Line"] = straight_lines_button
        

        #
        #   RUBBER BUTTON
        #
        rubber_button = Gtk.Button()
        
        img = Gtk.Image()
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size("icons/eraser.png", 28, 28)
        img.set_from_pixbuf(pixbuf)
        rubber_button.set_image(img)
        
        tools_grid.attach(rubber_button, 3, 0, 1, 1)
        rubber_button.connect("clicked", self.rubber_button_clicked)
        rubber_button.set_tooltip_text("Pick rubber, Ctrl+R")
        self.tools_button["Rubber"] = rubber_button
        
        #
        #   SPIN BUTTON (FOR CHANGING SIZE OF BRUSH)
        #
        adjustment1 = Gtk.Adjustment(value=1, lower=1, upper=30, step_increment=1, page_increment=5)
        spin_button = Gtk.SpinButton()
        spin_button.set_adjustment(adjustment1)
        spin_button.set_value(controller.get_brush_size())
        spin_button.connect("value-changed", self.controller.on_brush_size_changed)
        tools_grid.attach(spin_button, 1, 1, 1, 1)
        
        #
        #   SPIN BUTTON (FOR CHANGING SIZE OF LINE)
        #
        adjustment2 = Gtk.Adjustment(value=3, lower=3, upper=15, step_increment=2, page_increment=5)
        spin_button = Gtk.SpinButton()
        spin_button.set_adjustment(adjustment2)
        spin_button.set_value(controller.get_line_size())
        spin_button.connect("value-changed", self.controller.on_line_size_changed)
        tools_grid.attach(spin_button, 2, 1, 1, 1)
        
        #
        #   SPIN BUTTON (FOR CHANGING SIZE OF RUBBER)
        #
        adjustment3 = Gtk.Adjustment(value=5, lower=5, upper=50, step_increment=5, page_increment=5)
        rubber = Gtk.SpinButton()
        rubber.set_adjustment(adjustment3)
        rubber.set_value(controller.get_rubber_size())
        rubber.connect("value-changed", self.controller.on_rubber_size_changed)
        tools_grid.attach(rubber, 3, 1, 1, 1)
        
        #
        #   CLEAR CANVAS BUTTON
        #
        clear_button = Gtk.Button()
        
        img = Gtk.Image()
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size("icons/broom.png", 28, 28)
        img.set_from_pixbuf(pixbuf)
        clear_button.set_image(img)
        
        clear_button.connect("clicked", self.controller.on_clear_canvas)
        clear_button.set_tooltip_text("Clear canvas layer, Ctrl+C")
        tools_grid.attach(clear_button, 4, 0, 1, 1)
        self.tools_button["clean_canvas"] = clear_button
        
        #
        #   DELETE BY CLICK RUBBER BUTTON
        #
        check_button = Gtk.CheckButton(label="Delete by click")
        check_button.connect("toggled", self.on_checkbutton_toggled)
        check_button.set_tooltip_text("Enable Delete by click mode")
        tools_grid.attach(check_button, 3, 2, 1, 1)
        
        #
        #   MOVE OBJECTS BUTTON
        #
        move_objects = Gtk.ToggleButton()
        
        img = Gtk.Image()
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size("icons/arrow.png", 28, 28)
        img.set_from_pixbuf(pixbuf)
        move_objects.set_image(img)
        
        move_objects.connect("toggled", self.move_objects_mode)
        move_objects.set_tooltip_text("Move objects by click")
        tools_grid.attach(move_objects, 5, 0, 1, 1)
        self.tools_button["Move objects"] = move_objects
        
        #
        #   SHOW GRID BUTTON
        #
        show_grid = Gtk.ToggleButton()
        
        img = Gtk.Image()
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size("icons/grid.png", 28, 28)
        img.set_from_pixbuf(pixbuf)
        show_grid.set_image(img)
        
        show_grid.connect("toggled", self.show_grid_clicked)
        show_grid.set_tooltip_text("Shows squared grid on the draw area")
        tools_grid.attach(show_grid, 6, 0, 1, 1)
        self.tools_button["Grid"] = show_grid

        
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
            
            .solid-border {
                border: 2px solid black;
            }
        """)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
    
        self.connect("key-press-event", self.on_key_press)
        self.connect("delete-event", self.on_window_close)

##################################################################################
#   TOOL BUTTONS                                                                 #
##################################################################################

    def on_color_button_clicked(self, button, color):
        """Handle color button clicks to set the brush color."""
        self.controller.set_color(color)
        self.last_color = color
        # Reset all color button borders
        for name, btn in self.color_buttons.items():
            btn.get_style_context().remove_class("solid-border")
            
         # Reset all tool button borders
        for name, btn in self.tools_button.items():
            if(name != "Brush" and name != "Line"):
                btn.get_style_context().remove_class("solid-border")
        
        # Apply solid border to the clicked button
        button.get_style_context().add_class("solid-border")

        # Update CSS for solid border
        css_provider = Gtk.CssProvider()
        css_data = b"""
            .solid-border {
                border: 2px solid black;
            }
        """
        css_provider.load_from_data(css_data)
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

        for i in enumerate(self.color_palette):
            if color == i[1][1]:
                print("clicked:", i[1][0])
                self.last_color_button = i[1][0].lower()
                break
        
    def brush_button_clicked(self, button):
        """Brush button clicked. Sets style, when user clicks on it"""
        self.controller.clicked_brush()
        
        # Reset all tool button borders
        for name, btn in self.tools_button.items():
            btn.get_style_context().remove_class("solid-border")
            if(name == "Move objects"):
                btn.set_active(False)
                    
        # Apply solid border to the clicked button
        button.get_style_context().add_class("solid-border")

        # Update CSS for solid border
        css_provider = Gtk.CssProvider()
        css_data = b"""
            .solid-border {
                border: 2px solid black;
            }
        """
        css_provider.load_from_data(css_data)
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)
        
    def draw_lines_clicked(self, button):
        """Draw lines button clicked. Sets style, when user clicks on it"""
        self.controller.clicked_straight_lines()
        
        # Reset all tool button borders
        for name, btn in self.tools_button.items():
            btn.get_style_context().remove_class("solid-border")
            if(name == "Move objects"):
                btn.set_active(False)
            
        # Apply solid border to the clicked button
        button.get_style_context().add_class("solid-border")

        # Update CSS for solid border
        css_provider = Gtk.CssProvider()
        css_data = b"""
            .solid-border {
                border: 2px solid black;
            }
        """
        css_provider.load_from_data(css_data)
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

    def rubber_button_clicked(self, button):
        """Rubber button clicked. Sets style, when user clicks on it"""
        self.controller.clicked_rubber()
        
        # Reset all tool button borders
        for name, btn in self.tools_button.items():
            btn.get_style_context().remove_class("solid-border")
            if(name == "Move objects"):
                btn.set_active(False)
            
        for name, btn in self.color_buttons.items():
            btn.get_style_context().remove_class("solid-border")
        
        # Apply solid border to the clicked button
        button.get_style_context().add_class("solid-border")

        # Update CSS for solid border
        css_provider = Gtk.CssProvider()
        css_data = b"""
            .solid-border {
                border: 2px solid black;
            }
        """
        css_provider.load_from_data(css_data)
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

    def on_checkbutton_toggled(self, widget):
        """Handler for Delete by click rubber mode"""
        if widget.get_active():
            self.controller.checkbutton_clicked("enable")
        else:
            self.controller.checkbutton_clicked("disable")
        
    def move_objects_mode(self, button):
        """Handler for moving lines"""
        self.controller.is_moving_mode = button.get_active()
        self.controller.move_objects_mode()
        
         # Reset all tool button borders
        for name, btn in self.tools_button.items():
            btn.get_style_context().remove_class("solid-border")
            
        # Apply solid border to the clicked button
        #button.get_style_context().add_class("solid-border")
        
        # Update CSS for solid border
        css_provider = Gtk.CssProvider()
        css_data = b"""
            .solid-border {
                border: 2px solid black;
            }
        """
        css_provider.load_from_data(css_data)
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)
       
    def show_grid_clicked(self, button):
        """Handler for showing grid"""
        self.controller.show_grid_clicked()

##################################################################################
 

##################################################################################
#   INTERACTION WITH APPLICATION
##################################################################################

    def on_tip_clicked(self, widget):
        """Information about useful tips for user"""
        dialog = Gtk.MessageDialog(self, 
                                   Gtk.DialogFlags.MODAL, 
                                   Gtk.MessageType.INFO, 
                                   Gtk.ButtonsType.OK, 
                                   "Useful tips how to draw fast")
        
        dialog.format_secondary_text("List of shortcuts:\n\
Ctrl + B: to use Brush\n\
Ctrl + L: to draw straight Lines\n\
Ctrl + R: to use Rubber\n\
Ctrl + C: to clean Canvas\n\
Ctrl + S: to Save changes\n\
Ctrl + Z: to undo changes\n\
Ctrl + Y: to redo changes\n\
Ctrl + G: shows grid\n")
        
        dialog.run()
        dialog.destroy()
      
    def on_window_close(self, widget, event):
        """Dialog when user tries to close the application window"""
        dialog = Gtk.MessageDialog(
            parent=self,
            modal=True,
            destroy_with_parent=True,
            message_type=Gtk.MessageType.WARNING,
            buttons=Gtk.ButtonsType.NONE,
            text="You are about to exit the program.",
        )
        dialog.format_secondary_text("Do you want to save changes?")

        dialog.add_buttons(
            "Save and Leave", Gtk.ResponseType.OK,
            "Leave without saving", Gtk.ResponseType.NO,
            "Cancel", Gtk.ResponseType.CANCEL,
        )

        if(self.controller.get_saving_state() is True):
            Gtk.main_quit()
        else:
            dialog.connect("key-press-event", self.on_dialog_key_press)

            response = dialog.run()
            dialog.destroy()
            
            if response == Gtk.ResponseType.OK:
                print("The user has been saved and exited")
                if(self.controller.get_saving_state() is False and len(self.controller.get_saved_path()) != 0):
                    self.controller.quick_save_canvas()
                    Gtk.main_quit()
                else:
                    self.show_save_dialog("leave")
                return True
            elif response == Gtk.ResponseType.NO:
                print("The user confirmed the exit")
                Gtk.main_quit()
            else:
                return True
            
    def on_dialog_key_press(self, dialog, event):
        """Only for on_window_close"""
        if event.keyval == 65307:   # ESC
            print("The ESC key is pressed. Close the dialog.")
        
            dialog.destroy()

    def on_key_press(self, widget, event):
        """Handler for shortcuts"""
        
        # Get the name of the key
        keyval_name = Gdk.keyval_name(event.keyval)
        state = event.state

        if state & Gdk.ModifierType.CONTROL_MASK and (keyval_name == "b" or keyval_name == "B"):
            print("Ctrl+B pressed - activate Brush")
            # Simulate a button press
            button = self.tools_button.get("Brush")
            col_button = self.color_buttons.get(self.last_color_button.lower())
            
            if button:
                button.emit("clicked")
                if self.last_color:
                    print(f"Restore last color: {self.last_color}")
                    self.on_color_button_clicked(col_button, self.last_color)
                else:
                    print("There is no last color, so set black")
                    default_color = Gdk.RGBA(0, 0, 0, 1)
                    self.on_color_button_clicked(self.color_buttons['black'], default_color)
        elif state & Gdk.ModifierType.CONTROL_MASK and (keyval_name == "l" or keyval_name == "L"):
            print("Ctrl+L pressed - activate Line")
            # Simulate a button press
            button = self.tools_button.get("Line")
            col_button = self.color_buttons.get(self.last_color_button.lower())
            
            if button:
                button.emit("clicked")
                if self.last_color:
                    print(f"Restore last color: {self.last_color}")
                    self.on_color_button_clicked(col_button, self.last_color)
                else:
                    print("There is no last color, so set black")
                    default_color = Gdk.RGBA(0, 0, 0, 1)
                    self.on_color_button_clicked(self.color_buttons['black'], default_color)
        elif state & Gdk.ModifierType.CONTROL_MASK and (keyval_name == "r" or keyval_name == "R"):
            print("Ctrl+R pressed - activate Rubber")
            button = self.tools_button.get("Rubber")
            if button:
                button.emit("clicked")
        elif state & Gdk.ModifierType.CONTROL_MASK and (keyval_name == "c" or keyval_name == "C"):
            print("Ctrl+E pressed - activate Clean Canvas")
            button = self.tools_button.get("clean_canvas")
            if button:
                button.emit("clicked")
        elif state & Gdk.ModifierType.CONTROL_MASK and (keyval_name == "s" or keyval_name == "S"):
            print("Ctrl+S pressed - activate saving of the drawing")
            self.ctrls_clicked()
        elif state & Gdk.ModifierType.CONTROL_MASK and (keyval_name == "z" or keyval_name == "Z"):
            print("Ctrl+Z pressed - activate UNDO")
            button = self.tools_button.get("Undo")
            if button:
                button.emit("activate") 
        elif state & Gdk.ModifierType.CONTROL_MASK and (keyval_name == "y" or keyval_name == "Y"):
            print("Ctrl+Y pressed - activate REDO")
            button = self.tools_button.get("Redo")
            if button:
                button.emit("activate")
        elif state & Gdk.ModifierType.CONTROL_MASK and (keyval_name == "g" or keyval_name == "G"):
            print("Ctrl+G pressed - activate GRID")
            button = self.tools_button.get("Grid")
            if button:
                button.emit("activate")
        
        return False  # False allows the event to be passed on, True blocks it
        
    def on_new_menu_item_clicked(self, menu_item):
        """New choise in File menu handler. Used for reopen the application"""
        print("New menu item selected")
        dialog = Gtk.MessageDialog(
            parent=self,
            modal=True,
            destroy_with_parent=True,
            message_type=Gtk.MessageType.WARNING,
            buttons=Gtk.ButtonsType.NONE,
            text="You are about to create a new file.",
        )
        dialog.format_secondary_text("Do you want to save changes before creating a new file?")

        dialog.add_buttons(
            "Save and Create", Gtk.ResponseType.OK,
            "Create without saving", Gtk.ResponseType.NO,
            "Cancel", Gtk.ResponseType.CANCEL,
        )

        if(self.controller.get_saving_state() is True):
            self.controller.set_saving_state(False)
            self.controller.set_saved_path("", "")
            #self.controller.clear_canvas()
            self.controller.set_loaded_state(False)
            os.execv(sys.executable, [sys.executable] + sys.argv)
        else:
            dialog.connect("key-press-event", self.on_dialog_key_press)
            
            response = dialog.run()
            dialog.destroy()
            
            if response == Gtk.ResponseType.OK:
                print("The user has been saved and exited")
                self.show_save_dialog("new")
                return True
            elif response == Gtk.ResponseType.NO:
                print("The user confirmed the exit")
                self.controller.set_saving_state(False)
                self.controller.set_saved_path("", "")
                #self.controller.clear_canvas()
                self.controller.set_loaded_state(False)
                os.execv(sys.executable, [sys.executable] + sys.argv)
            else:
                return True

    def on_open_menu_item_clicked(self, menu_item):
        """Open choise in File menu handler. Used for import images"""
        print("Open menu item selected")
        dialog = Gtk.FileChooserDialog(
            title="Open File",
            parent=self,
            action=Gtk.FileChooserAction.OPEN,
            buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        )
        png_filter = Gtk.FileFilter()
        png_filter.set_name("PNG files")
        png_filter.add_pattern("*.png")
        dialog.add_filter(png_filter)
        
        filter_jpeg = Gtk.FileFilter()
        filter_jpeg.set_name("JPEG files")
        filter_jpeg.add_pattern("*.jpeg")
        dialog.add_filter(filter_jpeg)
        
        filter_json = Gtk.FileFilter()
        filter_json.set_name("JSON files")
        filter_json.add_pattern("*.json")
        dialog.add_filter(filter_json)
            

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            if(filename[-4] == "json"):
                type_format = "json"
            elif(filename[-4] == "jpeg"):
                type_format = "json"
            else:
                type_format = "png"
            self.controller.load_canvas(filename)
            self.controller.set_loaded_state(True)
            #self.controller.save_canvas(filename, type_format)
            self.controller.set_saved_path(filename, type_format)
            self.controller.set_saving_state(True)
        dialog.destroy()

    def on_save_menu_item_clicked(self, menu_item, type_format):
        """Save choise in File menu handler. Used to export image"""
        print("Save menu item selected:", type_format)
        dialog = Gtk.FileChooserDialog(
            title="Save As",
            parent=self,
            action=Gtk.FileChooserAction.SAVE,
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_SAVE, Gtk.ResponseType.OK,
        )
        
        dialog.connect("key-press-event", self.on_dialog_key_press)
        
        if(type_format == "png"):
            filter_png = Gtk.FileFilter()
            filter_png.set_name("PNG files")
            filter_png.add_pattern("*.png")
            dialog.add_filter(filter_png)
        elif(type_format == "jpeg"):
            filter_jpeg = Gtk.FileFilter()
            filter_jpeg.set_name("JPEG files")
            filter_jpeg.add_pattern("*.jpeg")
            dialog.add_filter(filter_jpeg)
        elif(type_format == "json"):
            filter_json = Gtk.FileFilter()
            filter_json.set_name("JSON files")
            filter_json.add_pattern("*.json")
            dialog.add_filter(filter_json)

        response = dialog.run()
        
        if response == Gtk.ResponseType.OK:
            file_path = dialog.get_filename()
            if(type_format == "png"):
                if not file_path.endswith(".png"):
                    file_path += ".png"  # Adding an extension if it is missing
            elif(type_format == "jpeg"):
                if not file_path.endswith(".jpeg"):
                    file_path += ".jpeg"
            elif(type_format == "json"):
                if not file_path.endswith(".json"):
                    file_path += ".json"
            self.controller.save_canvas(file_path, type_format)
            self.controller.set_saved_path(file_path, type_format)
            self.controller.set_saving_state(True)
        dialog.destroy()
        
    def on_quit_menu_item_clicked(self, menu_item):
        """Quit choise in File menu handler. Used to quit the application"""
        print("Quit menu item selected")
        dialog = Gtk.MessageDialog(
            parent=self,
            modal=True,
            destroy_with_parent=True,
            message_type=Gtk.MessageType.WARNING,
            buttons=Gtk.ButtonsType.NONE,
            text="You are about to exit the program.",
        )
        dialog.format_secondary_text("Do you want to save changes?")

        dialog.add_buttons(
            "Save and Leave", Gtk.ResponseType.OK,
            "Leave without saving", Gtk.ResponseType.NO,
            "Cancel", Gtk.ResponseType.CANCEL,
        )

        if(self.controller.get_saving_state() is True):
            Gtk.main_quit()
        else:
            dialog.connect("key-press-event", self.on_dialog_key_press)

            response = dialog.run()
            dialog.destroy()
            
            if response == Gtk.ResponseType.OK:
                print("The user has been saved and exited.")
                if(self.controller.get_saving_state() is False and len(self.controller.get_saved_path()) != 0):
                    self.controller.quick_save_canvas()
                    Gtk.main_quit()
                else:
                    self.show_save_dialog("leave")
                return True
            elif response == Gtk.ResponseType.NO:
                print("The user confirmed the exit.")
                Gtk.main_quit()
            else:
                return True
      
    def on_undo_menu_item_clicked(self, widget):
        """Undo shortcuts handler"""
        self.controller.on_undo_clicked()
        self.controller.set_saving_state(False)
        
    def on_redo_menu_item_clicked(self, widget):
        """Redo shortcuts handler"""
        self.controller.on_redo_clicked()
        self.controller.set_saving_state(False)
            
    def ctrls_clicked(self):
        """Handle Ctrl+S"""
        if(len(self.controller.get_saved_path()) == 0 and self.controller.get_saving_state() is False):
            self.show_save_dialog("save")
        elif(self.controller.get_saving_state() is False):
            print("CREATING QUICK SAVING")
            self.controller.quick_save_canvas()
        else:
            print(self.controller.get_saving_state())
            print(self.controller.get_saved_path())
    
    def show_save_dialog(self, mode):
        """Show small save dialog to choose format"""
        dialog = Gtk.Dialog(
            title="Save Picture",
            transient_for=self,
            modal=True,
        )
        dialog.set_default_size(300, 200)

        label = Gtk.Label(label="Select a save format:")
        label.set_margin_top(20)
        label.set_margin_bottom(10)
        label.set_margin_start(20)
        label.set_margin_end(20)
        dialog.get_content_area().add(label)

        # Add a drop-down list with options
        combo = Gtk.ComboBoxText()
        combo.append("png", "Save as PNG")
        combo.append("jpeg", "Save as JPEG")
        combo.append("json", "Save as JSON")
        combo.set_active(0)  # Set the first element as active
        combo.set_margin_bottom(10)
        dialog.get_content_area().add(combo)

        save_button = Gtk.Button(label="Save")
        cancel_button = Gtk.Button(label="Cancel")

        save_button.connect("clicked", lambda x: self.on_save_clicked(dialog, combo, mode))
        cancel_button.connect("clicked", lambda x: self.on_cancel_clicked(dialog))
        dialog.connect("key-press-event", self.on_dialog_key_press)

        button_box = Gtk.Box(spacing=10)
        button_box.set_halign(Gtk.Align.CENTER)
        button_box.set_margin_top(10)
        button_box.pack_start(save_button, True, True, 0)
        button_box.pack_start(cancel_button, True, True, 0)

        dialog.get_content_area().add(button_box)
        
        dialog.show_all()

    def on_save_clicked(self, dialog, combo, mode):
        """Hadle clicking save choice"""
        selected_format = combo.get_active_id()
        self.on_save_menu_item_clicked(dialog, selected_format)
        
        dialog.destroy()

        if(mode != "save"):
            self.final_words(mode)
        
    def final_words(self, mode):
        """Final words before closing dialog"""
        save_dialog = Gtk.MessageDialog(
            parent=self,
            modal=True,
            destroy_with_parent=True,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.NONE,
            text="Save confirmation",
        )
        save_dialog.format_secondary_text("Changes saved successfully")
        save_dialog.add_buttons(
            "OK", Gtk.ResponseType.YES,
        )

        response = save_dialog.run()
        save_dialog.destroy()

        if response == Gtk.ResponseType.YES:
            print("Data saved")
        
        if(mode == "leave"):
            Gtk.main_quit()
        elif(mode == "new"):
            self.controller.set_saving_state(False)
            self.controller.set_saved_path("", "")
            #self.controller.clear_canvas()
            self.controller.set_loaded_state(False)
            os.execv(sys.executable, [sys.executable] + sys.argv)
            
    def on_cancel_clicked(self, dialog):
        """Close saving window"""
        print("Operation cancelled")
        dialog.destroy()

##################################################################################

    def queue_draw(self):
        """Request redraw of the drawing area."""
        self.drawing_area.queue_draw()