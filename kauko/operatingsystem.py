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


# Mac
if sys.platform.startswith('darwin'):
    import osx
    _current_os = osx.OSX()

# Windows
elif os.name == 'nt':
    raise NotImplemented('Windows in not supported yet.')

# *nix(Linux etc.)
elif os.name == 'posix':
    import xlib
    _current_os = xlib.xlib()
#    raise NotImplemented('Linux in not supported yet.')


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
