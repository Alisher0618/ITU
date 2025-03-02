'''
    main.py
    Author: Alisher Mazhirinov, xmazhi00
    Main file for starting application
'''
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from model import PaintModel
from view import PaintView
from controller import PaintController

import signal
import sys


# Function for handling SIGINT signal (Ctrl+C)
def handle_sigint(signum, frame):
    """Function for handling SIGINT signal"""
    print("\nCtrl+C was pressed. Terminating the program..")
    sys.exit(0)

# Bind the handler to the SIGINT signal
signal.signal(signal.SIGINT, handle_sigint)

if __name__ == "__main__":
    model = PaintModel()
    controller = PaintController(model, None)  # Create controller without view initially
    view = PaintView(controller)
    controller.view = view  # Set view in controller

    view.connect("destroy", Gtk.main_quit)
    view.show_all()
    Gtk.main() # Main loop
