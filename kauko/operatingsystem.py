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


class BaseOS(object):
    """Base class for other OS classes."""

    def mouse_move(self, x, y, relative=True):
        """Moves mouse cursor to x, y in screen."""

        if relative:
            current_x, current_y = self._mouse.position()
            x = current_x + x
            y = current_y + y

        self._mouse.move(x, y)

    def mouse_click(self, button=1, double=False):
        """Emulates mouse button click. Default is left click.

        Kwargs:
            button: What button of the mouse to emulate.
                    Button is defined as 1 = left, 2 = right, 3 = middle.
        """
        x, y = self._mouse.position()
        if double:
            self._mouse.double_click(x, y, button=button)
        else:
            self._mouse.click(x, y, button=button)


# Mac
if sys.platform.startswith('darwin'):
    import osx
    _current_os = osx.OSX()

# Windows
elif os.name == 'nt':
    raise NotImplemented('Windows in not supported yet.')

# *nix(Linux etc.)
elif os.name == 'posix':
    import linux
    _current_os = linux.Linux()


def command(command, args, kwargs):
    """Returns success of command."""
    logger.info('%s %s %s' % (command, args, kwargs))

    if command not in ALLOWED_METHODS and command != BUTTON_PRESS_COMMAND:
        logger.warning('Unallowed method %s was called with %s %s' %
                       (command, args, kwargs))
        return False

    # Resolve the command from keymap
    if command == BUTTON_PRESS_COMMAND:
        button_id = str(args[0])
        try:
            command = settings['keymap'][button_id]
        except KeyError:
            msg = 'Error: Unknown button ID %s. It isn\'t specified in keymap.'
            logger.error(msg % button_id)
            return False

        # Remove the button_id from arguments that are given to method
        args = args[1:]

    try:
        method = getattr(_current_os, command)
    except AttributeError:
        return False

    return method(*args, **kwargs)
