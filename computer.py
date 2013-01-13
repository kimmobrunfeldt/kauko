"""
Classes to control the operating system.

The module level function named command handles the commanding of computer.
Module level variable _computer contains the instance of OS class.
It is chosen based on the currently running operating system.
"""

import os
import logging
import subprocess
import sys
import Quartz

logger = logging.getLogger(__name__)
script_dir = os.path.dirname(os.path.realpath(__file__))


# What are the allowed methods that JavaScript can call.
ALLOWED_METHODS = [
    'toggle_sleep_display',
    'volume_up',
    'volume_down',
    'next_track',
    'previous_track',
    'play_pause'
]


class ExampleOS(object):
    """Each OS class must provide the same public methods as this class."""
    def __init__(self):
        super(OSX, self).__init__()

    def toggle_sleep_display(self):
        """Toggles display between sleep and awake."""
        pass

    def volume_up(self):
        """Increases system volume."""
        pass

    def volume_down(self):
        """Decreases system volume."""
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


class OSX(object):
    """OSX specific."""

    # NSEvent.h
    NSSystemDefined = 14

    # hidsystem/ev_keymap.h
    NX_KEYTYPE_SOUND_UP = 0
    NX_KEYTYPE_SOUND_DOWN = 1
    NX_KEYTYPE_PLAY = 16
    NX_KEYTYPE_NEXT = 17
    NX_KEYTYPE_PREVIOUS = 18
    NX_KEYTYPE_FAST = 19
    NX_KEYTYPE_REWIND = 20

    def __init__(self):
        super(OSX, self).__init__()

    def _send_media_key(self, key):
        """Sends key using Quartz. Valid values are self.NX_KEYTYPE_...
        defined in this class.

        Main part taken from http://stackoverflow.com/questions/11045814/emulate-media-key-press-on-mac
        """
        def doKey(down):
            ev = Quartz.NSEvent.otherEventWithType_location_modifierFlags_timestamp_windowNumber_context_subtype_data1_data2_(
                self.NSSystemDefined,  # type
                (0, 0),  # location
                0xa00 if down else 0xb00,  # flags
                0,  # timestamp
                0,  # window
                0,  # ctx
                8,  # subtype
                (key << 16) | ((0xa if down else 0xb) << 8),  # data1
                -1  # data2
                )
            cev = ev.CGEvent()
            Quartz.CGEventPost(0, cev)

        doKey(True)
        doKey(False)

    # Public commands

    def toggle_sleep_display(self):
        display_is_asleep = Quartz.CGDisplayIsAsleep(0)

        program_path = os.path.join(script_dir, 'vendor/SleepDisplay')
        if not display_is_asleep:
            subprocess.call([program_path])

        else:
            subprocess.call([program_path, '--wake'])

    def volume_up(self):
        self._send_media_key(self.NX_KEYTYPE_SOUND_UP)

    def volume_down(self):
        self._send_media_key(self.NX_KEYTYPE_SOUND_DOWN)

    def previous_track(self):
        self._send_media_key(self.NX_KEYTYPE_REWIND)

    def next_track(self):
        self._send_media_key(self.NX_KEYTYPE_FAST)

    def play_pause(self):
        self._send_media_key(self.NX_KEYTYPE_PLAY)


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
    logger.info('%s %s %s' % (command, args, kwargs))

    if command not in ALLOWED_METHODS:
        return False

    try:
        method = getattr(_computer, command)
    except AttributeError:
        return False

    return method(*args, **kwargs)
