"""
Classes to control OS.
"""

import os


class ExampleOS(object):
    """Each OS class must provide the same public methods as this class."""
    def __init__(self):
        super(OSX, self).__init__()

    def mouse_move(self, x, y):
        """Moves mouse cursor to x, y in screen."""
        pass

    def mouse_click(self, button=0):
        """Emulates mouse button click. Default is left click.

        Kwargs:
            button: What button of the mouse to emulate. Valid numbers 0 - n.
                    Where n - 1 is the number of buttons in the mouse.
        """
        pass

    def send_key(self, key):
        """Emulates key press. Key """
        pass


class OSX(object):
    """OSX specific."""
    def __init__(self):
        super(OSX, self).__init__()

    def mouse_move(self, x, y):
        pass

    def mouse_click(self, button=0):
        pass

    def send_key(self, key):
        pass


