"""
Classes to control the operating system.

The module level function named command handles the commanding of computer.
Module level variable _computer contains the instance of OS class.
It is chosen based on the currently running operating system.
"""

import os
import logging
import sys

logger = logging.getLogger(__name__)
script_dir = os.path.dirname(os.path.realpath(__file__))


# What are the allowed methods that JavaScript can call.
ALLOWED_METHODS = [
    'toggle_sleep_display',
    'volume_up',
    'volume_down',
    'toggle_mute',
    'next_track',
    'previous_track',
    'play_pause',
    'send_key',
    'mouse_move',
    'mouse_click'
]


class ExampleOS(object):
    """Each OS class must provide the same public methods as this class."""
    def __init__(self):
        super(ExampleOS, self).__init__()

    def toggle_sleep_display(self):
        """Toggles display between sleep and awake."""
        pass

    def volume_up(self):
        """Increases system volume."""
        pass

    def volume_down(self):
        """Decreases system volume."""
        pass

    def toggle_mute(self):
        """Toggle mute."""
        pass

    def next_track(self):
        """Switches to next track."""
        pass

    def previous_track(self):
        """Switches to previous track."""
        pass

    def play_pause(self):
        """Play/pause media."""
        pass

    def send_key(self, key, is_key_code=False, is_ascii=False):
        """Simulates keypress.
        is_key_code: Is the key AppleScript's keycode?
        is_ascii: Is the key an ASCII character number?
        """
        pass

    def mouse_move(self, x, y, relative=True):
        """Moves mouse cursor to x, y in screen.
        If relative, moves cursor relative to current position.
        """

    def mouse_click(self, button=1, double=False):
        """Emulates mouse button click. Default is left click.

        Kwargs:
            button: What button of the mouse to emulate.
                    Button is defined as 1 = left, 2 = right, 3 = middle.
        """
        pass


class Mouse(object):
    """Taken from pymouse project.
    http://code.google.com/p/pymouse/
    """

    def press(self, x, y, button=1):
        """Press the mouse on a givven x, y and button.
        Button is defined as 1 = left, 2 = right, 3 = middle."""

        raise NotImplementedError

    def release(self, x, y, button=1):
        """Release the mouse on a givven x, y and button.
        Button is defined as 1 = left, 2 = right, 3 = middle."""

        raise NotImplementedError

    def click(self, x, y, button=1):
        """Click the mouse on a givven x, y and button.
        Button is defined as 1 = left, 2 = right, 3 = middle."""

        self.press(x, y, button)
        self.release(x, y, button)

    def move(self, x, y):
        """Move the mouse to a givven x and y"""

        raise NotImplementedError

    def position(self):
        """Get the current mouse position in pixels.
        Returns a tuple of 2 integers"""

        raise NotImplementedError

    def screen_size(self):
        """Get the current screen size in pixels.
        Returns a tuple of 2 integers"""

        raise NotImplementedError

    def double_click(self, x, y, button=1):
        raise NotImplementedError


# Mac
if sys.platform.startswith('darwin'):
    import osx
    _computer = osx.OSX()

# Windows
elif os.name == 'nt':
    raise NotImplemented('Windows in not supported yet.')

# *nix(Linux etc.)
elif os.name == 'posix':
    raise NotImplemented('Linux in not supported yet.')


def command(command, args, kwargs):
    """Returns success of command."""
    logger.info('%s %s %s' % (command, args, kwargs))

    if command not in ALLOWED_METHODS:
        logger.warning('Unallowed method %s was called with %s %s' %
                       (command, args, kwargs))
        return False

    try:
        method = getattr(_computer, command)
    except AttributeError:
        return False

    return method(*args, **kwargs)
