# main.py
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from model import PaintModel
from view_test import PaintView
from controller import PaintController

if __name__ == "__main__":
    model = PaintModel()
    controller = PaintController(model, None)  # Create controller without view initially
    view = PaintView(controller)
    controller.view = view  # Set view in controller

    view.connect("destroy", Gtk.main_quit)
    view.show_all()
    Gtk.main()
