"""
Classes to control OS.
"""

import os
import subprocess
import sys


import applescripts


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

    def _run(self, code):
        subprocess.call(['osascript', '-e', code])

    # Public commands

    def mouse_move(self, x, y):
        pass

    def mouse_click(self, button=0):
        pass

    def send_key(self, key):
        pass

    def volume_up(self):
        self._run(applescripts.volume_up)

    def volume_down(self):
        self._run(applescripts.volume_down)


# Mac
if sys.platform.startswith('darwin'):
    _computer = OSX()

# Windows
elif os.name == 'nt':
    raise NotImplemented('Windows in not supported yet.')

# *nix(Linux etc.)
elif os.name == 'posix':
    raise NotImplemented('Linux in not supported yet.')


def command(command, args, kwargs):
    """Returns success of command."""
    print command, args, kwargs

    try:
        method = getattr(_computer, command)
    except AttributeError:
        return False

    return method(*args, **kwargs)
