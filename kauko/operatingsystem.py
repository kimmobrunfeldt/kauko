"""
Classes to control the operating system.

The module level function named command handles the commanding of computer.
Module level variable _current_os contains the instance of OS class.
It is chosen based on the currently running operating system.
"""

import os
import logging
import sys

from settings import settings

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

# JavaScript can use this generic 'button_press' command when remote control's
# buttons are pressed. Also one parameter is given, the ID of the button.
# Button IDs and corresponding methods are defined in settings.json
BUTTON_PRESS_COMMAND = 'button_press'


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

    def send_key(self, key, is_ascii=False):
        """Simulates keypress.

        key: Single unicode character or ASCII number if is_ascii is True.
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


# Mac
if sys.platform.startswith('darwin'):
    import osx
    _current_os = osx.OSX()

# Windows
elif os.name == 'nt':
    raise NotImplemented('Windows in not supported yet.')

# *nix(Linux etc.)
elif os.name == 'posix':
    raise NotImplemented('Linux in not supported yet.')


def command(command, args, kwargs):
    """Returns success of command."""
    logger.info('%s %s %s' % (command, args, kwargs))

    if command not in ALLOWED_METHODS and command != BUTTON_PRESS_COMMAND:
        logger.warning('Unallowed method %s was called with %s %s' %
                       (command, args, kwargs))
        return False

    # Resolve the command from keymap
    if command == BUTTON_PRESS_COMMAND:
        button_id = args[0]
        command = settings['keymap'][button_id]

    try:
        method = getattr(_current_os, command)
    except AttributeError:
        return False

    return method(*args, **kwargs)
